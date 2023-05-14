from ghapi.all import GhApi
from datetime  import datetime
from pytz      import timezone

class ReadmeGenerator:
    def __init__(self, kullanici_adi:str, yildiza_gore_listele:bool=False, zaman_damgasi:bool=False, rozet:bool=False):
        self.api                  = self.github_api()
        self.kullanici_adi        = kullanici_adi
        self.yildiza_gore_listele = yildiza_gore_listele
        self.zaman_damgasi        = zaman_damgasi
        self.rozet                = rozet
        self.repolar              = [
            repo for repo in self.api.repos.list_for_user(username=self.kullanici_adi, per_page=100, sort="pushed")
                if repo.get("homepage") and repo.get("stargazers_count") > 3
        ]

        if self.yildiza_gore_listele:
            self.repolar = sorted(self.repolar, key=lambda veri: veri["stargazers_count"], reverse=True) 

        self.readme_olustur(kartlar=True)

    def github_api(self):
        # https://ghapi.fast.ai/fullapi.html
        # github_token = os.environ["GITHUB_TOKEN"]
        # api = GhApi(token=github_token)
        api = GhApi()
        return api

    def __tablo_olustur(self, kartlar:bool=False):
        readme = []

        if not kartlar:
            readme.extend((
                "| Yıldız |  Fork  |    Repo    |   Açıklama  |\n",
                "| ------ | ------ | ---------- | ----------- |\n"
            ))

        for repo in self.repolar:
            if repo["name"].lower().startswith("keyiflerolsun"):
                continue

            if kartlar:
                readme.append(f'<a href="{repo["html_url"]}" target="_blank"><img height="150px" width="45%" alt="{repo["name"]}" src="https://github-readme-stats.vercel.app/api/pin/?username={self.kullanici_adi}&repo={repo["name"]}&layout=compact&bg_color=2B2A29&text_color=FFF&title_color=EF7F1A&icon_color=EF7F1A&locale=tr"/></a> ')
                # readme.append(f'[![{repo["name"]}](https://github-readme-stats.vercel.app/api/pin/?username={self.kullanici_adi}&repo={repo["name"]}&layout=compact&bg_color=2B2A29&text_color=FFF&title_color=EF7F1A&icon_color=EF7F1A)]({repo["html_url"]})\n')
            else:
                readme.append(f"| {repo['stargazers_count']} | {repo['forks_count']} | [{repo['name']}]({repo['html_url']}) | {repo['description']} |\n")

        return readme

    def __readme_olustur(self, dosya, dosya_yolu:str, kartlar:bool):
        dosya.append(f"""\n\n  ---\n\n
<details align="center">
    <summary style="font-weight: bold; font-size: 18px">
        <b>Projeler</b>
        <i>(genişletmek için tıklayın!)</i>
    </summary>\n\n""")
        dosya.extend(self.__tablo_olustur(kartlar=kartlar))

        if self.rozet:
            dosya.append(f"\n\n[![Otomatik Profil Güncelleyici](https://github.com/{self.kullanici_adi}/{self.kullanici_adi}/actions/workflows/keyiflerolsun.yml/badge.svg)](https://github.com/{self.kullanici_adi}/{self.kullanici_adi}/actions/workflows/keyiflerolsun.yml)\n")

        if self.zaman_damgasi:
            dosya.append("\n\n\n")
            dosya.append(f"Son Güncelleme: {datetime.now(timezone('Turkey')).strftime('%d-%m-%Y %X')}\n")

        dosya.append("</details>")

        with open(dosya_yolu, "w", encoding="utf-8") as _dosya:
            _dosya.writelines(dosya)

    def readme_olustur(self, mevcut_dosya="__README.md", cikti_dosyasi="README.md", kartlar=False):
        with open(mevcut_dosya, encoding="utf-8") as _dosya:
            readme = _dosya.readlines()

        self.__readme_olustur(readme, cikti_dosyasi, kartlar)


if __name__ == "__main__":
    ReadmeGenerator(
        kullanici_adi        = "keyiflerolsun",
        yildiza_gore_listele = True, 
        zaman_damgasi        = True, 
        rozet                = True
    )
