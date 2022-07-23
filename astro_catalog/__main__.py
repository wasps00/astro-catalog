from . import step1, step2, step3, step4, step5, step6
from os.path import abspath

if __name__ == "__main__":
    # Subsample id
    n = 65
    # Step 1
    sample = step1.read_catalog("data_SDSS_Info.fit")
    subsample = step1.filter_catalog(sample, n)
    # Step 2 - 6
    for i, module in enumerate((step2, step3, step4, step5, step6)):
        module.main(sample, abspath(f"out/plot/step{i + 2}/sample/"))
        module.main(subsample, abspath(f"out/plot/step{i + 2}/subsample/"))
