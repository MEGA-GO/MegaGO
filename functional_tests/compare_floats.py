import pandas as pd
from io import StringIO
f_expect = '$expected_output_file'
df1 = pd.read_csv(StringIO('''$output'''))
df2 = pd.read_csv(f_expect)
try:
    pd.testing.assert_frame_equal(df1, df2, check_dtype=False)
except AssertionError as e:
    print(f"""
Tables are not equal!
left:\texpected output ({f_expect})
right:\tactual output

File comparison result (first unequal column):
{e}
        """)
