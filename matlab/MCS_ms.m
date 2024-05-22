function [States_Raw, Times_Raw, Initial_hour, state_now, state_next] = ...
  MCS_ms(n_Hr, TRM, Initial_hour,  state_now, state_next)

% Define local variables.
% ---------------------------------------------------------------------

n_com = length(TRM);
n_state_com = zeros(1,n_com);
for comp = 1 : n_com  
  n_state_com(comp) = length(TRM{comp});  
end

% Sample UP and DOWN times for each compoent:
for element = 1:n_com
  % This loop is for elements in the system.
  hour = Initial_hour(element);
  TTNE = zeros(1,n_state_com(element));  
  if hour >= n_Hr    
    States_Raw(element,1) = state_now(element)-1;
    Times_Raw(element , 1) = n_Hr;
    Initial_hour(element) = Initial_hour(element) - n_Hr;    
  else    
    if hour ~= 0      
      s = 2;
      States_Raw(element,1) = state_now(element)-1;
      Times_Raw(element , 1) = hour;
      state_now(element) = state_next(element);      
    else      
      s=1;      
    end    
    while hour<n_Hr
      % This loop is for the number of hours (we use hours and the output
      % is hour/year. If a daily index is needed, we use number of days
      % instead of number of hours)      
      for i = 1:n_state_com(element)        
        TTNE(i) = -log(rand)/(TRM{element}(state_now(element),i));        
      end      
      TTNE(TTNE <= 0 ) = NaN;
      [Time , state_next(element)] = min(TTNE);
      Time = round(Time,0); 
      if Time == 0        
        Time = 1;        
      end
      if Time ~= Inf        
        if hour + Time < n_Hr          
          States_Raw(element,s)=state_now(element)-1;
          hour = hour + Time;
          state_now(element) = state_next(element);
          Times_Raw(element,s) = Time;          
        else  
          remained_time = hour + Time - n_Hr;
          Times_Raw(element,s) = n_Hr - hour;
          States_Raw(element,s) = state_now(element) - 1;
          hour=n_Hr;          
        end
      else
        remained_time = 0;
        Times_Raw(element , s) = n_Hr-hour;
        States_Raw(element , s) = state_now(element)-1;
        hour=n_Hr;
      end
      s=s+1;
    end
    Initial_hour(element) = remained_time;
  end  
end

end