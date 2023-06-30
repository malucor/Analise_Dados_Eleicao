!pip install asn1crypto==1.5.1

import re
import pandas as pd
import seaborn as sns

# Exploração

!curl -s https://raw.githubusercontent.com/andre-marcos-perez/ebac-course-utils/develop/notebooks/2022_11_29/rdv.py -o rdv.py

!python rdv.py -r resultados.tse.jus.br_oficial_ele2022_arquivo-urna_407_dados_pe_25313_0149_0030_735931316f58456b68655a67706864613944794b6f422d7155453946325650384a434c454275306f5a44303d_o00407-2531301490030.rdv.txt > rdv.txt

content = []

with open(file="rdv.txt", mode="r") as fp:
  for line in fp.readlines():
    if "Governador" in line:
      break
    else:
      content.append(line)

len(content)

for line in content[0:10]:
  print(line)

pattern = re.compile(pattern="\[(.*?)\]")

votes = []

for line in content:
  if "branco" in line:
    votes.append({"voto": "branco", "quantidade": 1})
  if "nulo" in line:
    votes.append({"voto": "nulo", "quantidade": 1})
  if "nominal" in line:
    vote = re.findall(pattern=pattern, string=line)[0]
    votes.append({"voto": f"{vote}", "quantidade": 1})

len(votes)

for vote in votes[0:10]:
  print(vote)

# Processamento

votes_table = pd.DataFrame(votes)

votes_table.tail(n=30)

votes_table.shape

votes_table.to_csv("rdv.csv", header=True, index=False)

votes_table_agg = votes_table.groupby('voto').agg('sum').reset_index()

votes_table_agg

votes_table_agg = votes_table_agg.sort_values(by='quantidade', ascending=False)

votes_table_agg

votes_table_agg['quantidade_pct'] = round(100 * (votes_table_agg['quantidade'] / votes_table_agg['quantidade'].sum()), 2)

votes_table_agg

# Visualização

URNA = "Recife/PE - 149 - 30"

x_column = 'voto'
y_column = 'quantidade'

title = f'Apuração Presidente - Segundo turno de 2022 - Urna {URNA}'
x_lable = 'Voto'
y_lable = 'Quantidade'

with sns.axes_style('whitegrid'):
  chart = sns.barplot(data=votes_table_agg, x=x_column, y=y_column, palette='magma')
  chart.set(title=title, xlabel=x_lable, ylabel=y_lable);

x_column = 'voto'
y_column = 'quantidade_pct'

title = f'Apuração Presidente - Segundo turno de 2022 - Urna {URNA}'
x_lable = 'Voto'
y_lable = 'Quantidade (%)'

with sns.axes_style('whitegrid'):
  chart = sns.barplot(data=votes_table_agg, x=x_column, y=y_column, palette='magma')
  chart.set(title=title, xlabel=x_lable, ylabel=y_lable);