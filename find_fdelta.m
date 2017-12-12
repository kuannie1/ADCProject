function  [fdelta, h] = find_fdelta()
    y = read_file();
    plot(y)
    y_square = y.^2;
    fft_y2 = abs(fftshift(fft(y_square)));
    xaxis = linspace(-pi, (length(y_square) - 1) / length(y_square) * pi, length(y_square));
    [h_sq, idx] = max(fft_y2)
    theta = angle(xaxis(idx)) / 2;
    fdelta = xaxis(idx) / 2;
    h = sqrt(h_sq);
    for n=1:length(y)
        y(n) = y(n) / (h * exp(1i*(fdelta*n + theta)));
    end
end
function y = read_file()
    f1 = fopen('transmissiontest.dat', 'r');
    tmp = fread(f1,'float32');
    fclose(f1);
    y = tmp(1:2:end)+1i*tmp(2:2:end);
    %y = y(252800:end);
    %plot(real(y));
    y = y(252800 + 30 : 252800 + 612)
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