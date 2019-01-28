def count_totals(allcts):
    totals = dict()
    for cts in allcts:
        for n,ct in cts.items():
            if n not in totals.keys():
                totals[n] = 0
            totals[n] += ct
    return totals