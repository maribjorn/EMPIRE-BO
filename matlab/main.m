%  Parameters:
%--------------------------------------------------------------------------

n_ele = 4;
n_h = 8760;
Initial_hour(1:n_ele) = 0;
state_now(1:n_ele) = 1;
state_next(1:n_ele) = 1;
n_state_com = zeros(1,n_ele);

n_lines = 0;
n_CCGT = 0;
n_OCGT = 0;
n_solar = 0;
n_onwind = 0;
n_biomass = 0;
n_geo = 0;
n_ror = 0;
n_hydro = 0;
n_oil = 0;
n_y = 10;


%  Defining TRM (transition rate matrix) for all elements:
%--------------------------------------------------------------------------

TRM = cell(n_ele,1);

fr_PL             = [  -1/96264       	1/5000                     
                        1/9.5          -1/9.5       ];% checked 

fr_CCGT             = [  -1/96264       	1/5000                     
                        1/9.5          -1/9.5        	];% checked 

fr_OCGT             = [  -1/96264       	1/5000                     
                        1/9.5          -1/9.5       	];% checked 

fr_solar             = [  -1/96264       	1/5000                     
                        1/9.5          -1/9.5       	];% checked 

fr_onwind             = [  -1/96264       	1/5000                     
                        1/9.5          -1/9.5       	];% checked 

fr_biomass             = [  -1/96264       	1/5000                     
                        1/9.5          -1/9.5       	];% checked 

fr_geo             = [  -1/96264       	1/5000                     
                        1/9.5          -1/9.5        	];% checked 

fr_ror             = [  -1/96264       	1/5000                     
                        1/9.5          -1/9.5        	];% checked 

fr_hydro             = [  -1/96264       	1/5000                     
                        1/9.5          -1/9.5        	];% checked 

fr_oil             = [  -1/96264       	1/5000                     
                        1/9.5          -1/9.5        	];% checked 


for i = 1:num_lines
    fr_aux = fr_PL;
    fr_aux(1,2) = fr_aux(1,2)*length(i);
    TRM{i} = fr_aux; 
end

for i = 1:n_CCGT
    j = i+num_lines;
    TRM{j} = fr_CCGT;
end

for i = 1:n_OCGT
    j = i+num_lines+n_CCGT;
    TRM{j} = fr_OCGT;
end
for i = 1:n_solar
    j = i+num_lines+n_CCGT+n_OCGT;
    TRM{j} = fr_solar;
end
for i = 1:n_onwind
    j = i+num_lines+n_CCGT+n_OCGT+n_solar;
    TRM{j} = fr_onwind;
end
for i = 1:n_biomass
    j = i+num_lines+n_CCGT+n_OCGT+n_solar+n_onwind;
    TRM{j} = fr_biomass;
end
for i = 1:n_geo
    j = i+num_lines+n_CCGT+n_OCGT+n_solar+n_onwind+n_biomass;
    TRM{j} = fr_geo;
end
for i = 1:n_ror
    j = i+num_lines+n_CCGT+n_OCGT+n_solar+n_onwind+n_biomass+n_ror;
    TRM{j} = fr_ror;
end
for i = 1:n_hydro
    j = i+num_lines+n_CCGT+n_OCGT+n_solar+n_onwind+n_biomass+n_ror+n_hydro;
    TRM{j} = fr_hydro;
end
for i = 1:n_oil
    j = i+num_lines+n_CCGT+n_OCGT+n_solar+n_onwind+n_biomass+n_ror+n_hydro+n_oil;
    TRM{j} = fr_oil;
end


% MCS
% ----------------------------

for y = 1:n_y
  
  % Apply MCS to sample the state of the elemetns during a sample year.
  %------------------------------------------------------------------------
  [SR, TR, Initial_hour, state_now, state_next] = ...
  MCS_ms(n_h, TRM, Initial_hour, state_now, state_next);

  ST{y} = ArrangeStatesInTime(SR, TR, n_h, n_ele);

end



