function  [fdelta, h] = find_fdelta()
    y = read_file();
    y_square = y.^2;
    for k=1:450:length(y)
        start_index = k + 30
        if k+450-1 < length(y)
            end_index = k + 450 - 1 - 30;
        else
            end_index = length(y) - 30;
        end
        len = end_index - start_index + 1;
        
        fft_y2 = abs(fftshift(fft(y_square(start_index:end_index))));
        xaxis = linspace(-pi, (len - 1) / len * pi, len);
        [h_sq, idx] = max(fft_y2);
        theta = angle(xaxis(idx)) / 2;
        fdelta = xaxis(idx) / 2;
        h = sqrt(h_sq);
        for n=k:end_index+30
            y(n) = y(n) / (h * exp(1i*(fdelta*n + theta)));
        end
    end
    plot(real(y))
end
function y = read_file()
    f1 = fopen('rx.dat', 'r');
    tmp = fread(f1,'float32');
    fclose(f1);
    y = tmp(1:2:end)+1i*tmp(2:2:end);
    y = y(1634000+332:1634000+3314);
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