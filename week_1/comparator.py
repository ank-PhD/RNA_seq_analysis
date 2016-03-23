from pickle import load
import numpy as np
import pandas as pd
import seaborn as sns

cufflinks = load(open('cufflinks.dmp'))
my_pipe = load(open('my_pipe.dmp'))


for key, value in cufflinks.iteritems():
    cufflinks[key] = pd.DataFrame(data=value[:,1].astype(np.float32), index=value[:,0], columns=[key+'-c'])

cuff_list = cufflinks.values()
# print cuff_list[0]
df_cufflinks = cuff_list[0].join(cuff_list[1:])

for key, value in my_pipe.iteritems():
    value = np.array(value)
    pre_data = value[0, :, 1].astype(np.float32)
    # pre_data[np.isnan(pre_data)] = 0
    my_pipe[key] = pd.DataFrame(data=pre_data, index=value[0, :, 0],  columns=[key+'-m'])

my_list = my_pipe.values()
df_my_pipe = my_list[0].join(my_list[1:])

# print df_cufflinks

# print df_my_pipe

combined = df_my_pipe.join(df_cufflinks, how='left')

for i in range(1, 11):
    title = 't%s' % i
    sns.regplot(title+'-c', title+'-m', data=combined)
    sns.plt.savefig('corr-total.png')
    # sns.plt.clf()
    # sns.plt.show()
    # x = combined[title+'-c']
    # y = combined