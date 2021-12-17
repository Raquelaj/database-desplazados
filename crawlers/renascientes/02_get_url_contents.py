# -*- coding: utf-8 -*-

import time

from crawlers.model.post import Post, build_extracted_data_obj
from crawlers.persistence.dynamodb.dynamodb import query_post, save_post, is_post_extracted
from crawlers.renascientes.base import get_author, get_text, driver


for db_post in query_post("renascientes", False):

    post = Post.from_dict(db_post)

    if not is_post_extracted(post):
        print(post)

        driver.get(post.url)

        post.set_extracted_data(
            build_extracted_data_obj(get_author(), get_text())
        )

        save_post(post)

        time.sleep(5)

