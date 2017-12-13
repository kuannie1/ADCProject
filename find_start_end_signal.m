function y = find_start_end_signal()
    f1 = fopen('sixtythousandbits.dat', 'r');
    tmp = fread(f1,'float32');
    fclose(f1);
    y = tmp(1:2:end)+1i*tmp(2:2:end);
    
    real_y = real(y); % getting the real part of the y vector
    plot(real_y);
    
    length(real_y)
    
    start_of_signal = 0; % going to be the first index
    for i=2000:length(real_y)
      if (abs(real_y(i)) > 0.002)
        start_of_signal = i-5
        break
      end
    end
    
    end_of_signal = length(real_y);
    for i = length(real_y):-1:5
      if (abs(real_y(i)) > 0.002)
        end_of_signal = i+5
        break
      end
    end
    plot(real_y(start_of_signal:end_of_signal));
end