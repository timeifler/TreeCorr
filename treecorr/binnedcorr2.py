# Copyright (c) 2003-2014 by Mike Jarvis
#
# TreeCorr is free software: redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions, and the disclaimer given in the accompanying LICENSE
#    file.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions, and the disclaimer given in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the {organization} nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.


import treecorr

class BinnedCorr2(object):
    """This class stores the results of a 2-point correlation calculation, along with some
    ancillary data.

    This is a base class that is not intended to be constructed directly.  But it has a few
    helper functions that derived classes can use to help perform their calculations.  See
    the derived classes for more details:

        G2Correlation - handles shear-shear correlation functions
        N2Correlation - handles count-count correlation functions
        K2Correlation - handles kappa-kappa correlation functions
        NGCorrelation - handles count-shear correlation functions
        NKCorrelation - handles count-kappa correlation functions
        KGCorrelation - handles kappa-shear correlation functions

    Note that when we refer to kappa in the correlation function, that is because I
    come from a weak lensing perspective.  But really any scalar quantity may be used
    here.  CMB temperature fluctuations for example.

    The constructor for all derived classes take a config dict as the first argument,
    since this is often how we keep track of parameters, but if you don't want to 
    use one or if you want to change some parameters from what are in a config dict,
    then you can use normal kwargs, which take precedence over anything in the config dict.

    Exactly three of the following 4 parameters are required either in the config dict or
    in kwargs:

        nbins - How many bins to use
        bin_size - The width of the bins in log(separation)
        min_sep - The minimum separation; the left edge of the first bin
        max_sep - The maximum separation; the right edge of the last bin

    Any three of these may be provided.  The fourth number will be calculated from them.
    """
    def __init__(self, config=None, logger=None, **kwargs):
        import math
        if kwargs:
            import copy
            config = copy.copy(config)
            config.update(kwargs)
        self.config = config

        if logger is None:
            self.logger = treecorr.config.setup_logger(config.get('verbose',0),
                                                       config.get('log_file',None))
        else:
            self.logger = logger

        if 'x_col' not in config and 'sep_units' not in config:
            raise AttributeError("sep_units is required if not using x_col,y_col")
        sep_units = config.get('sep_units','arcsec')
        sep_units = treecorr.angle_units[sep_units]
        if 'nbins' not in self.config:
            if 'max_sep' not in self.config:
                raise AttributeError("Missing required parameter max_sep")
            if 'min_sep' not in self.config:
                raise AttributeError("Missing required parameter min_sep")
            if 'bin_size' not in self.config:
                raise AttributeError("Missing required parameter bin_size")
            self.min_sep = self.config['min_sep'] * sep_units
            self.max_sep = self.config['max_sep'] * sep_units
            self.bin_size = self.config['bin_size']
            self.nbins = int(math.ceil(math.log(self.max_sep/self.min_sep)/self.bin_size))
        elif 'bin_size' not in self.config:
            if 'max_sep' not in self.config:
                raise AttributeError("Missing required parameter max_sep")
            if 'min_sep' not in self.config:
                raise AttributeError("Missing required parameter min_sep")
            self.min_sep = self.config['min_sep'] * sep_units
            self.max_sep = self.config['max_sep'] * sep_units
            self.nbins = self.config['nbins']
            self.bin_size = math.log(self.max_sep/self.min_sep)/self.nbins
        elif 'max_sep' not in self.config:
            if 'min_sep' not in self.config:
                raise AttributeError("Missing required parameter min_sep")
            self.min_sep = self.config['min_sep'] * sep_units
            self.nbins = self.config['nbins']
            self.bin_size = self.config['bin_size']
            self.max_sep = exp(self.nbins*self.bin_size)*self.min_sep
        else:
            if 'min_sep' in self.config:
                raise AttributeError("Only 3 of min_sep, max_sep, bin_size, nbins are allowed.")
            self.max_sep = self.config['max_sep'] * sep_units
            self.nbins = self.config['nbins']
            self.bin_size = self.config['bin_size']
            self.min_sep = self.max_sep*exp(-self.nbins*self.bin_size)
        self.logger.info("nbins = %d, min,max sep = %e..%e radians, bin_size = %e",
                         self.nbins,self.min_sep,self.max_sep,self.bin_size)

        self.bin_slop = config.get('bin_slop', 1.0)

    def clear(self):
        """Clear the existing data array.  i.e. set all values to 0.
        """
        self.data[:] = 0


class G2Correlation(BinnedCorr2):
    """This class handles the calculation and storage of a 2-point shear-shear correlation
    function.
    """
    def __init__(self, config=None, logger=None, **kwargs):
        import numpy
        BinnedCorr2.__init__(self, config, logger=None, **kwargs)

        self.data = numpy.zeros(self.nbins, dtype=complex)

    def process(self, cat1, cat2=None):
        self.logger.info('Process G2 correlations...  or not.')

    def write(self, file_name):
        self.logger.info('Writing G2 correlations to %s',file_name)

    def writeM2(self, file_name):
        self.logger.info('Writing Map^2 from G2 correlations to %s',file_name)

class N2Correlation(BinnedCorr2):
    """This class handles the calculation and storage of a 2-point shear-shear correlation
    function.
    """
    def __init__(self, config=None, logger=None, **kwargs):
        import numpy
        BinnedCorr2.__init__(self, config, logger=None, **kwargs)

        self.data = numpy.zeros(self.nbins, dtype=float)

    def process(self, cat1, cat2=None):
        self.logger.info('Process N2 correlations...  or not.')

    def write(self, file_name, rr, dr=None, rd=None):
        self.logger.info('Writing N2 correlations to %s',file_name)


class K2Correlation(BinnedCorr2):
    """This class handles the calculation and storage of a 2-point shear-shear correlation
    function.
    """
    def __init__(self, config=None, logger=None, **kwargs):
        import numpy
        BinnedCorr2.__init__(self, config, logger=None, **kwargs)

        self.data = numpy.zeros(self.nbins, dtype=float)

    def process(self, cat1, cat2=None):
        self.logger.info('Process K2 correlations...  or not.')

    def write(self, file_name):
        self.logger.info('Writing K2 correlations to %s',file_name)


class NGCorrelation(BinnedCorr2):
    """This class handles the calculation and storage of a 2-point shear-shear correlation
    function.
    """
    def __init__(self, config=None, logger=None, **kwargs):
        import numpy
        BinnedCorr2.__init__(self, config, logger=None, **kwargs)

        self.data = numpy.zeros(self.nbins, dtype=complex)

    def process(self, cat1, cat2):
        self.logger.info('Process NG correlations...  or not.')

    def write(self, file_name, rg=None):
        self.logger.info('Writing NG correlations to %s',file_name)

    def writeNM(self, file_name, rg=None):
        self.logger.info('Writing NMap from NG correlations to %s',file_name)

    def writeNorm(self, file_name, gg, nn, rr, nr=None, rg=None):
        self.logger.info('Writing Norm from NG correlations to %s',file_name)


class NKCorrelation(BinnedCorr2):
    """This class handles the calculation and storage of a 2-point shear-shear correlation
    function.
    """
    def __init__(self, config=None, logger=None, **kwargs):
        import numpy
        BinnedCorr2.__init__(self, config, logger=None, **kwargs)

        self.data = numpy.zeros(self.nbins, dtype=float)

    def process(self, cat1, cat2):
        self.logger.info('Process NK correlations...  or not.')

    def write(self, file_name, rk=None):
        self.logger.info('Writing NK correlations to %s',file_name)


class KGCorrelation(BinnedCorr2):
    """This class handles the calculation and storage of a 2-point shear-shear correlation
    function.
    """
    def __init__(self, config=None, logger=None, **kwargs):
        import numpy
        BinnedCorr2.__init__(self, config, logger=None, **kwargs)

        self.data = numpy.zeros(self.nbins, dtype=complex)

    def process(self, cat1, cat2):
        self.logger.info('Process KG correlations...  or not.')

    def write(self, file_name):
        self.logger.info('Writing KG correlations to %s',file_name)
