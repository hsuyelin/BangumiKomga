# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description: Bangumi API(https://github.com/bangumi/api)
# ------------------------------------------------------------------


import requests
from requests.adapters import HTTPAdapter
from thefuzz import fuzz
from tools.log import logger
from zhconv import convert
from urllib.parse import quote_plus


class BangumiApi:
    BASE_URL = "https://api.bgm.tv"

    def __init__(self, access_token=None):
        self.r = requests.Session()
        self.r.mount('http://', HTTPAdapter(max_retries=3))
        self.r.mount('https://', HTTPAdapter(max_retries=3))
        self.access_token = access_token
        if self.access_token:
            self.refresh_token()

    def _get_headers(self):
        headers = {
            'User-Agent': 'chu-shen/BangumiKomga (https://github.com/chu-shen/BangumiKomga)'}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def refresh_token(self):
        # https://bgm.tv/dev/app
        # https://next.bgm.tv/demo/access-token
        return

    def compute_name_score_by_fuzzy(self, name, name_cn, infobox, target):
        """
        Use fuzzy to computes the Levenshtein distance between name, name_cn, and infobox "别名" (if exists) and the target string.
        """
        score = fuzz.ratio(name, target)
        if name_cn:
            score = max(score, fuzz.ratio(name_cn, target))
        for item in infobox:
            if item["key"] == "别名":
                if isinstance(item["value"], (list,)):  # 判断传入值是否为列表
                    for alias in item["value"]:
                        score = max(
                            score, fuzz.ratio(alias["v"], target))
                else:
                    score = max(
                        score, fuzz.ratio(item["value"], target))
        return score
        
    def search_subjects(self, query):
        '''
        获取搜索结果，并移除非漫画系列。返回具有完整元数据的条目
        '''
        query = convert(query, 'zh-cn')
        url = f"{self.BASE_URL}/search/subject/{quote_plus(query)}?responseGroup=small&type=1&max_results=25"
        # TODO 处理'citrus+ ~柑橘味香气plus~'
        try:
            response = self.r.get(url, headers=self._get_headers())
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            return []

        # e.g. Artbooks.VOL.14 -> {"request":"\/search\/subject\/Artbooks.VOL.14?responseGroup=large&type=1","code":404,"error":"Not Found"}
        try:
            response_json = response.json()
        except ValueError as e:
            # bangumi无结果但返回正常
            # logger.error(f"An error occurred: {e}")
            return []
        else:
            # e.g. 川瀬绫 -> {"results":1,"list":null}
            if "list" in response_json and isinstance(response_json["list"], (list,)):
                results = response_json["list"]
            else:
                return []

        # 具有完整元数据的排序条目，可提升结果准确性，但增加请求次数
        sort_results = []
        for result in results:
            manga_id = result['id']
            manga_metadata = self.get_subject_metadata(manga_id)
            if not manga_metadata:
                continue
            # bangumi书籍类型包括：漫画、小说、画集、其他
            # 由于komga不支持小说文字的读取，这里直接忽略`小说`类型，避免返回错误结果
            if manga_metadata["platform"] != "小说":
                single_flag = True
                for relation in self.get_related_subjects(manga_id):
                    # bangumi书籍系列包括：系列、单行本
                    # 此处需去除漫画系列的单行本，避免干扰
                    # bangumi数据中存在单行本与系列未建立联系的情况
                    if relation["relation"] == "系列":
                        single_flag = False
                        break
                if single_flag:
                    sort_results.append(manga_metadata)

        sort_results.sort(key=lambda x: self.compute_name_score_by_fuzzy(
            x["name"], x.get("name_cn", ""), x['infobox'], query),reverse=True)

        return sort_results

    def get_subject_metadata(self, subject_id):
        '''
        获取漫画元数据
        '''
        url = f"{self.BASE_URL}/v0/subjects/{subject_id}"
        try:
            response = self.r.get(url, headers=self._get_headers())
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            return []
        return response.json()

    def get_related_subjects(self, subject_id):
        '''
        获取漫画的关联条目
        '''
        url = f"{self.BASE_URL}/v0/subjects/{subject_id}/subjects"
        try:
            response = self.r.get(url, headers=self._get_headers())
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            return []
        return response.json()

    def update_reading_progress(self, subject_id, progress):
        '''
        更新漫画系列卷阅读进度
        '''
        url = f"{self.BASE_URL}/v0/users/-/collections/{subject_id}"
        payload = {
            "vol_status": progress
        }
        try:
            response = requests.patch(
                url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
        return response.status_code == 204


    def get_subject_thumbnail(self, subject_metadata):
        '''
        获取漫画封面
        '''
        try:
            thumbnail=requests.get(subject_metadata['images']['large']).content
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            return []
        files = {
            'file': (subject_metadata['name'], thumbnail)
        }
        return files