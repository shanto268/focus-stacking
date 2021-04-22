def getNeatTomograms(csvFile):
    I_matrices_reshaped = np.loadtxt(csvFile)

    filters = [
        'none', 'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36',
        'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'catrom',
        'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos'
    ]

    for j in range(len(filters)):
        dir_name = "/Users/sshanto/hep/hep_daq/CAMAC/focus-stacking/images/mystery_same_axis/{}".format(
            filters[j])
        mkdir_p(dir_name)
        k = 0
        print("Using {} filter".format(filters[j]))
        for i in I_matrices_reshaped:
            i = i.reshape(21, 21)
            fig = plt.figure(frameon=False)
            ax = plt.Axes(fig, [0., 0., 1., 1.])
            ax.set_axis_off()
            fig.add_axes(ax)
            imshowobj = ax.imshow(np.flip(i),
                                  aspect='auto',
                                  inerpolation=filters[j])
            imshowobj.set_clim(0.9, 1.2)
            fname = "{}/img{}.png".format(dir_name, k)
            fig.savefig(fname)
            k += 1
