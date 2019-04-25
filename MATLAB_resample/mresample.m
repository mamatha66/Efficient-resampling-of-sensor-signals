function exitcode = mresample(file_path, filename, current_frequency, target_frequency)
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
    xData = G.data(:,1)*uf;
    yData = G.data(:,2)*uf;
    zData = G.data(:,3)*uf;

    n = length(xData);
    p = str2num(target_frequency);
    q = str2num(current_frequency);
    % resample_factor = p/q;

    rxData = resample(xData',p,q);
    ryData = resample(yData',p,q);
    rzData = resample(zData',p,q);
    
    % Resampled signal
    rG(:,1) = rxData;
    rG(:,2) = ryData;
    rG(:,3) = rzData;

    dt = 1/q;
    t = 0:dt:(n-1)*dt;
    % rdt = 1/nfs;
    nn = length(rxData);
    rt = linspace(min(t),max(t), nn);

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
    plot(t,xData,'r')
    % plot(s,yData,'b')
    % plot(s,zData,'g')
    xlabel('Time (s)')
    ylabel('Acceleration (m/s2)')
    legend('x-axis', ...
        'Location','NorthEast')
    title('Original Signal')
    
    subplot(3,1,2);
    plot(rt,rxData,'r')
    % plot(u,ryData,'b')
    % plot(u,rzData,'g')
    xlabel('Time (s)')
    ylabel('Acceleration (m/s2)')
    legend('x-axis', ...
        'Location','NorthEast')
    title('Resampled Signal')
    
    subplot(3,1,3);
    plot(t,xdiff,'r')
    % plot(s,yDiff,'b')
    % plot(s,zDiff,'g')
    xlabel('Time (s)')
    ylabel('Acceleration (m/s2)')
    legend('x-axis', ...
        'Location','NorthEast')
    title('Difference between Original and Resampld Signals')
    
    exitcode = 0;

end