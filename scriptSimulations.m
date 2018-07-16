

clear

clc

%inceput must be greater or equal to 2

inceput = 2;

sfarsit = 2;

numarSimulari=100;


timpiProbabilisti = [];



%for i=inceput:sfarsit
    
    %for j=inceput:sfarsit
        
  
        partialTimes = [];
        dmpR = [];
        
        contor = 0;
        
        while contor < numarSimulari
            
            %taskSet = generateRandomTaskSetFunction(20, 2, 100);
            taskSet = givenTaskSetFunction(0, 0, 100, contor);
            
            if maxUtilization(taskSet) < 2 && maxUtilization(taskSet) > 1
                
                contor = contor+1;
                    
                tic;
                probRespTime = probabilisticWorstCaseResponseTime(taskSet, 1);
                toc;
                partialTimes(contor) = toc;                
                target = length(taskSet); 
                d=dmp(probRespTime,taskSet{target}{2});
                dmpR(contor)=dmpVal(d);
            end
            
        end
        format longE;
        timpiProbabilisti(2-inceput+1, 2-inceput+1) = mean(partialTimes);        
        %probRespTime
        
                
    %end
    
%end


format short;
disp('finished')
disp('The probabilistic Analysis lasts:')

timpiProbabilisti
