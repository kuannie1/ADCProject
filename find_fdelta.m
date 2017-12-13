function  [fdelta, h] = find_fdelta()
    y = read_file();
    y_square = y.^2;
%     for k=1:5000:length(y)
%         start_index = k;
%         if k+5000-1 < length(y)
%             end_index = k + 5000 - 1;
%         else
%             end_index = length(y);
%         end
%         len = end_index - start_index + 1;
        fft_y2 = abs(fftshift(fft(y_square)));
        xaxis = linspace(-pi, (length(y_square) - 1) / length(y_square) * pi, length(y_square));
%         fft_y2 = abs(fftshift(fft(y_square(start_index:end_index))));
%         xaxis = linspace(-pi, (len - 1) / len * pi, len);
        [h_sq, idx] = max(fft_y2);
        theta = angle(xaxis(idx)) / 2;
        fdelta = xaxis(idx) / 2;
        h = sqrt(h_sq);
%         for n=k:end_index
        for n=1:length(y_square)
            y(n) = y(n) / (h * exp(1i*(fdelta*n + theta)));
        end
%     end
    figure
    plot(real(y))
    
end
function y = read_file()
    f1 = fopen('sixtythousandbits.dat', 'r');
    tmp = fread(f1,'float32');
    fclose(f1);
    y = tmp(1:2:end)+1i*tmp(2:2:end);
    y = y(1076851+3031:4079857);
    %y = y(1116000+1104:1116000+1077000+1192);
    %a = length(y)
    plot(real(y));
%     real_y = real(y)
%     start_of_signal = 0
%     for i=1:length(real_y)
%         if abs(real_y(i)) > THRESHOLD:
%             start_of_signal = i - 2
%             break
%     
        
    
    %y =y(1018000+495:1044000+1476); % superlong50.dat
   % plot(real(y));
    %y = y(1005500+78:1005500+3057);
   % figure
    %plot(real(y));
%     y = y(1634000+332:1634000+3314);
%     plot(real(y));
    %y = y(252800:end);
    %plot(real(y));
%     y = y(252800 + 30 : 252800 + 612);
%     y = real(y);
%     for n=1:length(y)
%         if real(y(n)) > 1.5 * 10^-3
%             n
%             break
%         end
%     end
%     for n=length(y):-1:1
%         if real(y(n)) > 1.5 * 10^-3
%             n
%             break
%         end
%     end
end