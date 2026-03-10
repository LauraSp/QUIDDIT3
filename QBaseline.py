from QUtility import QUtility as QU
from QSettings import QSettings as QS
import numpy as np
import os
import scipy.optimize as op
import sys


def remove_baseline(filename, output_path, bl_type='standard'):
    """function to remove baseline from a diamond FTIR spectrum.

    Baseline removal can be performed in two ways: 'standard' and 'difference'.
    In the 'standard' method, the type IIa spectrum is fitted to the two-phonon
    region of   the sample spectrum and subtracted from the sample spectrum.
    In the 'difference' method, the type IIa spectrum is subtracted from the
    sample spectrum and a slope is fitted and removed from the resulting
    spectrum. The resulting spectrum is then saved to the output directory with
    a 'c' prefix added to the original filename.

    Parameters
    ----------
    filename : str
        Path to the input spectrum file.
    output_path : str
        Path to the output directory.
    bl_type : str, optional
        Type of baseline removal ('standard' or 'difference'). Default is
        'standard'.

    Returns
    -------
    None
    """

    # read type IIa spectrum
    IIa_spec = QU.read_spec(QS.IIa_path)

    # read sample spectrum
    spec_orig = QU.read_spec(filename)
    spec_orig = QU.spectrum_slice(spec_orig, 400, 7000)

    # preliminary baseline correction
    bl = -spec_orig[-1][1]
    spec_prelim_abs = spec_orig[:, 1] + bl

    spec_prelim = np.column_stack((spec_orig[:, 0], spec_prelim_abs))

    IIa_spec_ip = QU.inter(
        IIa_spec, spec_prelim[:, 0:-1], inttype='linear')

    print('preliminary correction...')
    if bl_type == 'standard':
        # Use average intensity over ±5 cm⁻¹ range around 1992 cm⁻¹
        # for robustness
        I_1992_avg = QU.average_intensity(1992, 10, spec_prelim)

        # Guard against noise-dominated spectra
        # min acceptable intensity at 1992cm⁻¹
        min_intensity_threshold = 0.01
        # max allowed scaling factor. 2000 is equivalent to a 50 micron thick
        # sample - is this a reasonable lower limit?
        max_factor_threshold = 2000.0

        if abs(I_1992_avg) < min_intensity_threshold:
            print('WARNING: Spectrum appears to be noise-dominated!')
            print(f'Average intensity around 1992 cm⁻¹ ({I_1992_avg:.3f}) '
                  f'is below threshold ({min_intensity_threshold})')
            print(
                'Skipping baseline correction and saving original spectrum...')

            # Save original spectrum with warning prefix
            failed_spec = os.path.join(
                output_path, ('noise_' + os.path.basename(filename)))
            np.savetxt(failed_spec, spec_orig, delimiter=',')
            print(f"Original spectrum saved as: {failed_spec}")
            return  # Exit early

        # calculate scaling factor
        factor = 12.3/abs(I_1992_avg)

        if factor > max_factor_threshold:
            print('WARNING: Calculated scaling factor '
                  f'({factor:.1f}) exceeds threshold ({max_factor_threshold})')
            print('This suggests the spectrum may be noise-dominated or have '
                  'poor signal quality')
            print(
                'Skipping baseline correction and saving original spectrum...')

            # Save original spectrum with warning prefix
            failed_spec = os.path.join(
                output_path, ('noise_' + os.path.basename(filename)))
            np.savetxt(failed_spec, spec_orig, delimiter=',')
            print(f"Original spectrum saved as: {failed_spec}")
            return  # Exit early

        print(f'Scaling factor: {factor:.2f} '
              f'(avg intensity 1987-1997 cm⁻¹: {I_1992_avg:.3f})')
        spec_prelim[:, 1] *= factor

        two_phonon_left = QU.spectrum_slice(spec_prelim, 1500, 2312)
        two_phonon_right = QU.spectrum_slice(spec_prelim, 2391, 3000)
        two_phonon_extra = QU.spectrum_slice(spec_prelim, 3800, 4000)
        two_phonon = np.vstack(
            (two_phonon_left, two_phonon_right, two_phonon_extra))

        two_phonon_wav = np.arange(
            two_phonon[:, 0][0], two_phonon[:, 0][-1], 0.1)

        # interpolate slice of spectrum used for fitting
        two_phonon_ip = QU.inter(
            spec_prelim, two_phonon_wav, inttype='linear')

        # interpolate relevant area of type IIa spectrum
        IIa_spec_ip_new = QU.inter(
            IIa_spec, two_phonon_wav, inttype='linear')

        # arguments needed for IIa_fit
        IIa_args = (two_phonon_wav, two_phonon_ip, IIa_spec_ip_new)

        # initial guess of parameters (normf, poly1, poly2)
        IIa_x0 = (1, 0, 0)

        # (min, max)-pairs for parameters
        IIa_bounds = [(0.0, None), (None, None), (None, None)]

        # fit type IIa spectrum to two-phonon region of sample spectrum
        IIa_res = op.minimize(
            QU.IIa,
            args=IIa_args,
            x0=IIa_x0,
            method='L-BFGS-B',
            bounds=IIa_bounds
            )

        print(IIa_res)

        # Check if the fit was successful
        if not IIa_res.success:
            print("WARNING: IIa spectrum fit did not converge successfully!")
            print(f"Fit message: {IIa_res.message}")
            print("Saving original spectrum as fallback...")

            # Save the original spectrum with 'failed_' prefix
            failed_spec = os.path.join(
                output_path, ('failed_' + os.path.basename(filename)))
            np.savetxt(failed_spec, spec_orig, delimiter=',')
            print(f"Original spectrum saved as: {failed_spec}")

        fit_IIa = QU.IIa_fit(
            IIa_res.x,
            spec_prelim[:, 0].reshape(len(spec_prelim[:, 0]), 1),
            spec_prelim[:, 1].reshape(len(spec_prelim[:, 1]), 1)
            )
        abs_temp = fit_IIa - IIa_spec_ip

        spec_final = np.column_stack((spec_prelim[:, 0], abs_temp))

    elif bl_type == 'difference':
        I_2670 = QU.height(2670, spec_prelim)
        I_2442 = QU.height(2442, spec_prelim)

        dist = I_2442 - I_2670
        target_dist = 4
        factor = target_dist/dist

        # preliminary baseline correction
        spec_prelim[:, 1] *= factor

        # interpolate type IIa spectrum to sample spectrum wavenumbers
        IIa_spec_ip = QU.inter(
            IIa_spec, spec_prelim[:, 0:-1], inttype='linear')

        new_abs = spec_prelim[:, 1] - IIa_spec_ip.flatten()
        new_spec = np.column_stack((spec_prelim[:, 0], new_abs))

        sloping_area_left = QU.spectrum_slice(new_spec, 1400, 7000)
        sloping_area = np.vstack((sloping_area_left, new_spec[-1]))

        poly_params = np.polyfit(sloping_area[:, 0], sloping_area[:, 1], 1)

        linear_baseline = np.polyval(poly_params, new_spec[:, 0])

        abs_final = new_spec[:, 1] - linear_baseline

        spec_final = np.column_stack((new_spec[:, 0], abs_final))

    else:
        print("BL type not recognised")

    print('saving spectrum after IIa subtraction...')

    new_spec = os.path.join(output_path, ('c'+os.path.basename(filename)))
    np.savetxt(new_spec, spec_final, delimiter=',')

    print(60 * '-')


if __name__ == "__main__":
    remove_baseline(sys.argv[1], sys.argv[2], sys.argv[3])
