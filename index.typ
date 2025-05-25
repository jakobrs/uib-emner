#let data = csv("out.csv")

#table(columns: (auto, 1fr), [*Emnekode*], [*Tittel*], ..data.map(row => (upper(row.at(0)), link("https://www4.uib.no/studier/emner/" + row.at(0), row.at(1)))).flatten())
