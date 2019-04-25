function exitcode = resample(file_path, filename, current_frequency, target_frequency)
    % clear all;
    clc;
    file = fullfile(file_path, filename);
    if exist(file, 'file')
       fopen(file);
    else
        warningMessage = sprintf('%s does not exist', file);
        uiwait(warndlg(warningMessage));
    end
    G = importdata(filename);

    uf = 9.8/2^12;
    xData = G.data(:,1) * uf;
    yData = G.data(:,2) * uf;
    zData = G.data(:,3) * uf;

    n = length(xData);
    fs = str2num(current_frequency);
    nfs = str2num(target_frequency);
    k = nfs/fs;

    dt = 1/fs;
    t = 0:dt:(n-1)*dt;

    if k > 1
        % Interpolatio by a factor of k
        rxData = sinc_interp1(xData,k);
        ryData = sinc_interp1(yData,k);
        rzData = sinc_interp1(zData,k);

    else
        [L,M] = rat(nfs/fs);
        if L == 1
            % Decimating by a factor of L
            rxData = decimate1(xData,M);
            ryData = decimate1(yData,M);
            rzData = decimate1(zData,M);

        else
            % Interpolating by a factor of L
            rxData = sinc_interp1(xData,L);
            ryData = sinc_interp1(yData,L);
            rzData = sinc_interp1(zData,L);

    
           % Decimating by a factor of M
           rxData = decimate1(rxData,M);
           ryData = decimate1(ryData,M);
           rzData = decimate1(rzData,M);
        end
    end

    nn = length(rxData);
    rt = linspace(min(t),max(t), nn);
    
    % Resampled signal
    rG(:,1) = rxData;
    rG(:,2) = ryData;
    rG(:,3) = rzData;

    xres = interp1(rt,rxData,t);
    xdiff = xres' - xData;
    mean_error_xaxis = sum(xdiff)/length(xdiff)

    yres = interp1(rt,ryData,t);
    ydiff = yres' - yData;
    mean_error_yaxis = sum(ydiff)/length(ydiff);

    zres = interp1(rt,rzData,t);
    zdiff = zres' - zData;
    mean_error_zaxis = sum(zdiff)/length(zdiff);
    
    % Difference between Original and Resampled signals
    D(:,1) = xdiff;
    D(:,2) = ydiff;
    D(:,3) = zdiff;

    subplot(3,1,1);
    plot(t,xData,'m')
    % plot(s,yData,'b')
    % plot(s,zData,'g')
    xlabel('Time (s)')
    ylabel('Acceleration (m/s2)')
    legend('x-axis', ...
        'Location','NorthEast')
    title('Original Signal')

    subplot(3,1,2);
    plot(rt,rxData,'m')
    % plot(u,ryData,'b')
    % plot(u,rzData,'g')
    xlabel('Time (s)')
    ylabel('Acceleration (m/s2)')
    legend('x-axis', ...
        'Location','NorthEast')
    title('Resampled Signal')

    subplot(3,1,3);
    plot(t,xdiff,'m')
    % plot(s,yDiff,'b')
    % plot(s,zDiff,'g')
    xlabel('Time (s)')
    ylabel('Acceleration (m/s2)')
    legend('x-axis', ...
        'Location','NorthEast')
    title('Difference between Original and Resampld Signals')
    % suptitle(['Sensor signal with ', num2str(n), 'samples, sampled at ', num2str(fs), 'Hz is resampled to ', num2str(nfs), 'Hz'])
    
    exitcode = 0;

end