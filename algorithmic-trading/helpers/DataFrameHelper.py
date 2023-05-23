import pandas as pd

# https://note.nkmk.me/en/python-pandas-option-setting/
# https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html
display_settings = {
    'max_columns': 10,
    'expand_frame_repr': False,  # Wrap to multiple pages
    'max_rows': 20,
    'precision': 2,
    'show_dimensions': True
}


def set_data_frame_options():
    for op, value in display_settings.items():
        pd.set_option("display.{}".format(op), value)

