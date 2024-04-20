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
            f"\n   title = {{\emph{{{page_title}}}}}," \
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
