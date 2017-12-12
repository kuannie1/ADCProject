function y = find_start_end_signal()
    f1 = fopen('superlong50.dat', 'r');
    tmp = fread(f1,'float32');
    fclose(f1);
    y = tmp(1:2:end)+1i*tmp(2:2:end);
    
    real_y = real(y); % getting the real part of the y vector
    start_of_signal = 0; % going to be the first index
    for i=1:length(real_y)
      if (abs(real_y(i)) > 0.0025)
        start_of_signal = i-3;
        break
      end
    end
    
    end_of_signal = length(real_y);
    for i = length(real_y):-1:1
      if (abs(real_y(i)) > 0.0025)
        end_of_signal = i+3;
        break
      end
    end
    plot(real_y(start_of_signal:end_of_signal));
    figure 
    plot(real_y(start_of_signal-10000:end_of_signal+10000));
end