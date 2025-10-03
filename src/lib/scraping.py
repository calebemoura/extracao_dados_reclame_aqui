from playwright.sync_api import sync_playwright
from lxml import etree 
from datetime import datetime
from lib.upload import upload_to_databricks
from lib.normalize import normalize_text

# Parser para interpretar o HTML
myparser = etree.HTMLParser(encoding="utf-8")

def scraping_reclame_aqui(
        nome_empresa: str,
        token: str,
        volume_path: str,
        host_databriks: str
    ) -> None:
    
    """
    Esta função realiza os seguintes passos:
    --> Realizar scraping de reclamações no site Reclame Aqui
    --> Realiza upload dos dados coletados para um volume do Databricks
    --> Parâmetros: 
        nome_empresa: Nome da empresa a ser pesquisada no Reclame Aqui (colocar o nome como está no site)
        token: Token de autenticação para o Databricks
        volume_path: Caminho do volume no Databricks onde os dados serão armazenados
        host: URL do host do Databricks
    """

    empresa = normalize_text(nome_empresa)

    # Início da automação com Playwright
    with sync_playwright() as p:
        # Cria uma instância do navegador Chromium
        browser = p.chromium.launch(
            headless=False,
            slow_mo=700
        )

        # Cria um novo contexto de navegador com configurações específicas
        context = browser.new_context(
            accept_downloads=True,
            java_script_enabled=True,
            base_url="https://www.reclameaqui.com.br/"
        )

        # Abre uma nova página no contexto do navegador
        page = context.new_page()
        page.goto(f"/empresa/{empresa}/lista-reclamacoes/?pagina=1", timeout=1200000, wait_until='load')

        lista_reclamacoes = []
        dados_reclamacoes = []
        cont = True

        while cont:

            html_content = page.content()
            tree = etree.HTML(html_content, parser=myparser)
            reclamacoes = tree.xpath('//div[@class="sc-1sm4sxr-0 iwOeoe"]//a/@href')
            [lista_reclamacoes.append(r) for r in reclamacoes]

            if len(reclamacoes) != 0:
                for url in lista_reclamacoes:
                    context.clear_cookies()
                    page_1 = context.new_page()
                    page_1.goto(url, timeout=120000, wait_until='load')

                    html_content = page_1.content()
                    tree = etree.HTML(html_content, parser=myparser)
                    reclmacao = tree.xpath('//div[@data-testid="complaint-content-container"]')
                    find_text = etree.XPath("string()")

                    for r in reclmacao:
                        titulo = r.xpath('//h1[@data-testid="complaint-title"]')
                        empresa = r.xpath('//a[@data-testid="company-page-link"]')
                        local = r.xpath('//span[@data-testid="complaint-location"]')
                        data = r.xpath('//span[@data-testid="complaint-creation-date"]')
                        id = r.xpath('//span[@data-testid="complaint-id"]/text()')
                        status = r.xpath('//span[contains(@class, "sc-1a60wwz-1")]')
                        texto = r.xpath('//p[@data-testid="complaint-description"]')
                        resposta = r.xpath('//span[@class="sc-1o3atjt-3 bHNkuv"]')

                        dados_reclamacoes.append(
                            { 
                                'titulo': find_text(titulo[0]).strip(),
                                'empresa': find_text(empresa[0]).strip(),
                                'local': find_text(local[0]).strip(),
                                'dataReclamacao': find_text(data[0]).strip(),
                                'idReclamacao': id[0].strip(),
                                'status': find_text(status[0]).strip(),
                                'reclamacao': find_text(texto[0]).strip(),
                                'dataResposta': find_text(resposta[0]).strip() if len(resposta) > 0 else None,
                                'urlReclamacao': page_1.url
                            }
                        )

                    page_1.wait_for_timeout(10000)
                    page_1.close()

                upload_to_databricks(
                    data=dados_reclamacoes,
                    token=token,
                    volume_path=volume_path,
                    file_name=f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    host=host_databriks
                )

                lista_reclamacoes.clear()
                dados_reclamacoes.clear()

                btn_next = page.locator('//*[@id="__next"]/div[3]/div/div/main/section[2]/div[2]/div[2]/div[11]/div/button[3]')

                if btn_next.is_visible():
                    btn_next.click()
                    page.wait_for_timeout(10000)
                else:
                    page.close()
                    break
            else:
                cont = False
                page.close()

        context.close()
        browser.close()