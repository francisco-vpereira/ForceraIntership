import os

def website_noauthor_apa(org_name="",year="", page_title="", url="", last=""):
    """
    Arguments:
        org_name: organization name
        year: year of publication
        page_title: name of the page
        url: website URL
        last: date last accessed

    return: string containing website with no author defined reference in APA format
    """

    apa = org_name + '. (' + year + '). ' + page_title + '. Retrieved from ' + url + '. Last accessed ' + last + '.'
    return apa
    


def website_noauthor_bib(name="",org_name="",year="", page_title="", url="", last=""):
    """
    Arguments:
        org_name: organization name
        year: year of publication
        page_title: name of the page
        url: website URL
        last: date last accessed

    return: string containing website with no author defined reference in BibTex format
    """

    bibtex = f"@misc{{{name},\n   author = {{{org_name}}}," \
            f"\n   title = {{{{{page_title}}}}}," \
            f"\n   year = {{{year}}}," \
            f"\n   note = {{Último acesso em {last}}}," \
            f"\n   howpublished = {{Disponível em \\url{{{url}}}}}" \
            f"\n}}"
            
    file_path = "/home/francisco/MECAD/2º Ano/Estágio/tese/tese_pt/thesis-bib.bib"
    with open(file_path, "a") as bib_file:
        bib_file.write(bibtex + '\n\n')

    return bibtex

# -------------------------------------------#
# Limpar ficheiro para não reescrever citações
# -------------------------------------------#
file_path = "/home/francisco/MECAD/2º Ano/Estágio/tese/tese_pt/thesis-bib.bib"
with open(file_path, "w") as bib_file:
    bib_file.write('')


# -------------------------------------------#
# Código dos Contratos Públicos e Relacionados
#--------------------------------------------#
guia_poise = website_noauthor_bib(name="guia_poise",
                                org_name="Programa Operacional Inclusão Social e Emprego (PO ISE)",
                                year=2022,
                                page_title="Guia de Contratação Pública",
                                url="https://poise.portugal2020.pt/documents/10180/123741/Guia+de+Contrata%C3%A7%C3%A3o+P%C3%BAblica_PO+ISE_maio+2022.pdf/002e4f48-4c1d-4cb5-92e9-4f7a039762d9",
                                last="15/04/2024"
                                )



ccp = website_noauthor_bib(name="ccp",
                        org_name="Código dos Contratos Públicos (CCP)",
                        year=2023,
                        page_title="Decreto-Lei n.º 18/2008, de 29 de janeiro",
                        url="https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2008-34455475",
                        last="15/04/2024"
                        )



lex = website_noauthor_bib(name="lex",
                        org_name="Código dos Contratos Públicos (CCP)",
                        year=2023,
                        page_title="Decreto-Lei n.º 18/2008, de 29 de janeiro",
                        url="https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2008-34455475",
                        last="15/04/2024"
                        )



corrections = website_noauthor_bib(name="corrections",
                        org_name="Comissão Europeia",
                        year=2019,
                        page_title="Commission Decision of 14.5.2019 laying down the guidelines for determining financial corrections to be made to expenditure financed by the Union for non - compliance with the applicable rules on public procurement",
                        url="https://ec.europa.eu/regional_policy/en/information/publications/decisions/2019/commission-decision-of-14-5-2019-laying-down-the-guidelines-for-determining-financial-corrections-to-be-made-to-expenditure-financed-by-the-union-for-non-compliance-with-the-applicable-rules-on-public-procurement",
                        last="17/04/2024"
                        )

programaproc = website_noauthor_bib(name="programaproc",
                        org_name="Diário da República",
                        year="",
                        page_title="Programa do procedimento",
                        url="https://diariodarepublica.pt/dr/lexionario/termo/programa-procedimento",
                        last="19/04/2024"
                        )

caderno = website_noauthor_bib(name="caderno",
                        org_name="Diário da República",
                        year="",
                        page_title="Caderno de Encargos",
                        url="https://diariodarepublica.pt/dr/lexionario/termo/caderno-encargos",
                        last="19/04/2024"
                        )

ue_dire = website_noauthor_bib(name="ue_dire",
                        org_name="Parlamento Europeu",
                        year="2024",
                        page_title="Diretiva 2014/24/UE do Parlamento Europeu e do Conselho, de 26 de fevereiro de 2014 , relativa aos contratos públicos e que revoga a Diretiva 2004/18/CE Texto relevante para efeitos do EEE",
                        url="https://eur-lex.europa.eu/eli/dir/2014/24/oj/por",
                        last="20/04/2024"
                        )

ajustedir = website_noauthor_bib(name="ajustedir",
                        org_name="Diário da República",
                        year="",
                        page_title="Ajuste Direto",
                        url="https://diariodarepublica.pt/dr/lexionario/termo/ajuste-direto",
                        last="22/04/2024"
                        )

consultaprev = website_noauthor_bib(name="consultaprev",
                        org_name="Diário da República",
                        year="",
                        page_title="Consulta Prévia",
                        url="https://diariodarepublica.pt/dr/lexionario/termo/consulta-previa",
                        last="22/04/2024"
                        )

concursopub = website_noauthor_bib(name="concursopub",
                        org_name="Diário da República",
                        year="",
                        page_title="Concurso Público",
                        url="https://diariodarepublica.pt/dr/lexionario/termo/concurso-publico",
                        last="22/04/2024"
                        )


previaqual = website_noauthor_bib(name="previaqual",
                        org_name="Diário da República",
                        year="",
                        page_title="Concurso Limitado por Prévia Qualificação",
                        url="https://diariodarepublica.pt/dr/lexionario/termo/concurso-limitado-por-previa-qualificacao",
                        last="22/04/2024"
                        )

dialogoconc = website_noauthor_bib(name="dialogoconc",
                        org_name="Diário da República",
                        year="",
                        page_title="Diálogo Concorrencial",
                        url="https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2008-34455475-44688075",
                        last="22/04/2024"
                        )

acordoquadro = website_noauthor_bib(name="acordoquadro",
                        org_name="Diário da República",
                        year="",
                        page_title="Acordo Quadro",
                        url="https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2008-34455475-108092895",
                        last="22/04/2024"
                        )


mistos = website_noauthor_bib(name="mistos",
                        org_name="Diário da República",
                        year="",
                        page_title="Contratos Mistos",
                        url="https://diariodarepublica.pt/dr/lexionario/termo/contratos-mistos-contratacao-publica",
                        last="22/04/2024"
                        )


jardinagem = website_noauthor_bib(name="jardinagem",
                        org_name="Portal BASE",
                        year="",
                        page_title="Detalhes contratuais",
                        url="https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id=9536560",
                        last="30/04/2024"
                        )

# ------------------------------------------#
# Open Contracting Partnership e Relacionados
#-------------------------------------------#

ocp = website_noauthor_bib(name="ocp",
                        org_name="Open Contracting Partnership",
                        year=2016,
                        page_title="Better procurement for people and the planet.",
                        url="https://www.open-contracting.org/",
                        last="15/04/2024"
                        )

resource = website_noauthor_bib(name="resource",
                        org_name="Open Contracting Partnership",
                        year=2016,
                        page_title="",
                        url="https://www.open-contracting.org/resources/?tab=resource-library",
                        last="15/04/2024"
                        )                                

redflags_guide = website_noauthor_bib(name="redflags_guide",
                                    org_name="Open Contracting Partnership",
                                    year=2016,
                                    page_title="Red Flags for integrity: Giving the green light to open data solution",
                                    url="https://www.open-contracting.org/wp-content/uploads/2016/11/OCP2016-Red-flags-for-integrityshared-1.pdf",
                                    last="15/04/2024"
                                )



ocp_brief = website_noauthor_bib(name="ocp_brief",
                                org_name="Open Contracting Partnership",
                                year=2016,
                                page_title="Why open contracting is essential to open government",
                                url="https://www.open-contracting.org/resources/why-open-contracting-is-essential-to-open-government/",
                                last="15/04/2024"
                                )

transparency = website_noauthor_bib(name="transparency",
                                org_name="Open Contracting Partnership",
                                year=2016,
                                page_title="Open Contracting: A New Frontier for Transparency and Accountability",
                                url="https://www.open-contracting.org/resources/open-contracting-a-new-frontier-for-transparency-and-accountability/",
                                last="15/04/2024"
                                )

ocp_guide = website_noauthor_bib(name="ocp_guide",
                                org_name="Open Contracting Partnership",
                                year=2016,
                                page_title="Open Contracting Guide",
                                url="https://www.open-contracting.org/resources/open-contracting-guide/",
                                last="15/04/2024"
                                )

report2017 = website_noauthor_bib(name="report2017",
                                org_name="Open Contracting Partnership",
                                year=2017,
                                page_title="Annual Report 2017: Serving up transparency and change in public contracting",
                                url="https://www.open-contracting.org/resources/annual-report-2017-serving-transparency-change-public-contracting/",
                                last="15/04/2024"
                                )

report2018 = website_noauthor_bib(name="report2018",
                                org_name="Open Contracting Partnership",
                                year=2018,
                                page_title="Annual Report 2018",
                                url="https://www.open-contracting.org/resources/annual-report-2018/",
                                last="15/04/2024"
                                )

report2019 = website_noauthor_bib(name="report2019",
                                org_name="Open Contracting Partnership",
                                year=2019,
                                page_title="Annual Report 2019",
                                url="https://www.open-contracting.org/resources/annual-report-2019/",
                                last="15/04/2024"
                                )

report2020 = website_noauthor_bib(name="report2020",
                                org_name="Open Contracting Partnership",
                                year=2020,
                                page_title="Annual Report 2020",
                                url="https://www.open-contracting.org/resources/annual-report-2020/",
                                last="15/04/2024"
                                )

report2021 = website_noauthor_bib(name="report2021",
                                org_name="Open Contracting Partnership",
                                year=2021,
                                page_title="Annual Report 2021",
                                url="https://www.open-contracting.org/resources/annual-report-2021/",
                                last="15/04/2024"
                                )

idiot_guide = website_noauthor_bib(name="idiot_guide",
                                org_name="Open Contracting Partnership",
                                year=2021,
                                page_title="Idiot’s Guide to Looting Public Procurement and Get Rich Quick",
                                url="https://www.open-contracting.org/resources/idiotsguide/",
                                last="15/04/2024"
                                )


spreadsheet = website_noauthor_bib(name="spreadsheet",
                                org_name="Open Contracting Partnership",
                                year=2021,
                                page_title="Using open contracting data",
                                url="https://www.open-contracting.org/data/data-use/#tools",
                                last="20/04/2024"
                                )

spreadsheet1 = website_noauthor_bib(name="spreadsheet1",
                                org_name="Open Contracting Partnership",
                                year=2021,
                                page_title="Red Flags to OCDS Mapping",
                                url="https://docs.google.com/spreadsheets/d/12PFkUlQH09jQvcnORjcbh9-8d-NnIuk4mAQwdGiXeSM/edit#gid=2027439485",
                                last="20/04/2024"
                                )                        




# ---------------------------------------------- #
#           Math + Python + PostgreSQL           #
# ---------------------------------------------- #

casella = '@book{casella2002statistical, title={Statistical Inference},author={Casella, G. and Berger, R.L.},isbn={9780534243128},lccn={20010257},series={Duxbury advanced series in statistics and decision sciences},url={"https://books.google.pt/books?id=0x_vAAAAMAAJ"},year={2002},publisher={Thomson Learning}}'
with open(file_path, "a") as bib_file:
        bib_file.write(casella + '\n\n')

ross = '@book{ross2014introduction,title={Introduction to Probability and Statistics for Engineers and Scientists},author={Ross, S.M.},isbn={9780123948427},lccn={2014011941},url={https://books.google.pt/books?id=BaPOv33uZCMC},year={2014},publisher={Elsevier Science}}'
with open(file_path, "a") as bib_file:
        bib_file.write(ross + '\n\n')

spe = '@book{spe,title={Outliers em Dados Estatísticos},author={Fernando Rosado},url={https://www.spestatistica.pt/publicacoes/publicacao/outliers-em-dados-estatisticos},year={2006},publisher={Sociedade Portuguesa de Estatística}}'
with open(file_path, "a") as bib_file:
        bib_file.write(spe + '\n\n')

python = '@book{python,title={Programming in Python 3: A Complete Introduction to the Python Language},author={Summerfield, M.},isbn={9780321680563},lccn={2009035430},series={Developer\'s library},url={https://books.google.pt/books?id=H9emM_LGFDEC},year={2010},publisher={Addison-Wesley}}'
with open(file_path, "a") as bib_file:
        bib_file.write(python + '\n\n')

postgre = '@book{sql,title={Practical PostgreSQL},author={Drake, J.D. and Worsley, J.C.},isbn={9781449310288},lccn={2002283901},url={https://books.google.pt/books?id=fI1lAgAAQBAJ},year={2002},publisher={O\'Reilly Media}}'
with open(file_path, "a") as bib_file:
        bib_file.write(postgre + '\n\n')

skew = '@article{HUBERT20085186,title = {An adjusted boxplot for skewed distributions},journal = {Computational Statistics & Data Analysis},volume = {52},number = {12},pages = {5186-5201},year = {2008},issn = {0167-9473},doi = {https://doi.org/10.1016/j.csda.2007.11.008},url = {https://www.sciencedirect.com/science/article/pii/S0167947307004434},author = {M. Hubert and E. Vandervieren},abstract = {The boxplot is a very popular graphical tool for visualizing the distribution of continuous unimodal data. It shows information about the location, spread, skewness as well as the tails of the data. However, when the data are skewed, usually many points exceed the whiskers and are often erroneously declared as outliers. An adjustment of the boxplot is presented that includes a robust measure of skewness in the determination of the whiskers. This results in a more accurate representation of the data and of possible outliers. Consequently, this adjusted boxplot can also be used as a fast and automatic outlier detection tool without making any parametric assumption about the distribution of the bulk of the data. Several examples and simulation results show the advantages of this new procedure.}}'
with open(file_path, "a") as bib_file:
        bib_file.write(skew + '\n\n')