 function [State_Time] = ArrangeStatesInTime(State_Raw,Time_Raw, n_Hr,n_com)


    
        D = [];
        C = [];
        D1 = [];
        A = Time_Raw;
    
        % This loop calculates cumulative Times
        for j = 1:n_com
        
            for i = 2:size(Time_Raw,2)-1
            
                A(j,i) = A(j,i) + A(j,i-1);
            
            end
        
            A(j,size(Time_Raw,2))  = n_Hr;
        
        end
        
        % Sort and delete repetitive times
        B = sort(A);
        C(1,:) = unique(B);
        D(n_com+1,:) = [0,C];

        % This part calculates the states of the system with related times. 
        D(1:n_com,1) = State_Raw(:,1);
        
        for i = 1:length(C)-1
            
            D(1:n_com,i+1) = D(1:n_com,i);
            [row,col] = find(A==C(i));
            
            if length(row) == 1
                
                D(row,i+1) = State_Raw(row,col+1);
                
            else
                
                for j = 1:length(row)
                    
                    D(row(j),i+1) = State_Raw(row(j),col(j)+1);  
                    
                end
                
            end
            
        end
        
        D(1:n_com,length(C)+1) = D(1:n_com,length(C));

%         States_Time1{year,1} = D;    

        
        % This part deletes the similar consecutive states. 
        s=1;
        D1(:,1) = D(:,1);
        
        for i = 1:size(D,2)-1
   
            if sum(D(1:n_com,i) - D(1:n_com,i+1)) ~= 0
        
                s = s+1;
                D1(:,s) = D(:,i+1);
        
            end

        end

        D1(:,end+1) = D(:,end);
        State_Time = D1;
    
end



