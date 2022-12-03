largest_n = 3
with open("input.txt") as f:
  totals = [0]
  for l in f.readlines():
    if l == "\n":
      totals.append(0)
    else:
      totals[len(totals) - 1] += int(l)
  ordered = sorted(totals, reverse=True)
  print(sum(ordered[:largest_n]))