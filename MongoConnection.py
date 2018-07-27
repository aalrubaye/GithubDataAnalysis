from pymongo import MongoClient
import powerlaw as pl
import matplotlib.pyplot as plt

__author__ = 'Abdul Rubaye'


def connect():
    client = MongoClient()
    database = client.github_16
    # final_collection = database.final_collection
    collection = database.collection_no_noise
    return collection

#plot diagrams using the powerlaw lib
try:
    Degree = open('/Users/Abduljaleel/Desktop/full_normal_t3.txt', 'r')
    data = []
    for row in Degree:
        if row != '':
            data.append(int(row))
    print data

    # # fit = pl.Fit(data)
    # fit = pl.Fit(data, discrete=True)
    # print str(fit.power_law.alpha)

    fit = pl.Fit(data)
    fit.plot_pdf(marker='o',linestyle='none',color='black', markersize=15)
    fit.power_law.plot_pdf(label=r'$\alpha = %.2f\pm%.3f$'%(fit.power_law.alpha,2*fit.power_law.sigma),color='red',lw=3)
    plt.legend(loc='best', fontsize= 24)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.show()

except:
    print 'ERROR'
