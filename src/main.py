import constants.constants as constants
import utils.utils as utils


if __name__ == "__main__":

    df = utils.read_data(constants.ACTIVITY_DATA)

    utils.print_first_n_rows(df, 5)
    utils.print_shape(df)
    utils.print_info(df)
    utils.print_summary(df)
