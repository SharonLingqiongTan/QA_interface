def count(handler, uid, dh):
    lemur = solr = terrier = findmore_blue = findmore_pink =   0
    for line in handler:
        if line.startswith('query/lemur'): lemur += 1
        elif line.startswith('query/solr'): solr += 1
        elif line.startswith('query/terrier'): terrier += 1
        elif line.startswith('findmore/pink'): findmore_pink += 1
        elif line.startswith('findmore/blue'): findmore_blue += 1
    dh.write(','.join(['assr'+str(uid)]+[str(c) for c in [lemur, solr, terrier, findmore_pink, findmore_blue]])+'\n\n')


dh = open('ModeUsageStat.csv','w')
dh.write('user,lemur,solr,terrier,findmore_pink,findmore_blue\n\n')
for uid in range(1, 7):
    fh = open('./dump/assr'+str(uid)+'.log','r')
    count(fh, uid, dh)
    fh.close()
dh.close()


