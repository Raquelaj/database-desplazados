    #
    #
    # for k, article in enumerate(articles):
    #
    #     print(k)
    #
    #     if "text" in article.keys():
    #         continue
    #
    #     driver.get(article['url'])
    #     title = driver.find_element_by_css_selector("#component > main > article > header > h3").text
    #     text = driver.find_element_by_css_selector("#component > main > article > div.item_fulltext").text
    #
    #     try:
    #         author = driver.find_element_by_css_selector(
    #             "#component > main > article > div.item_info > dl > dd:nth-child(2) > address").text
    #     except:
    #         author = "N/A"
    #
    #     print(title)
    #
    #     if text == '':
    #         try:
    #             time.sleep(5)
    #             download_iframe_pdf()
    #         except NoSuchElementException:
    #             try:
    #                 driver.find_element_by_css_selector("#pa-deny-btn").click()
    #                 download_iframe_pdf()
    #             except:
    #                 continue
    #
    #         text = "PDF Text"
    #
    #     article["title"] = title
    #     article["text"] = text
    #     article["author"] = author
    #
    #     if k % 10 == 9:
    #         with open(f"{filename.split('.')[0]}.json", "w") as json_file:
    #             json_file.write(json.dumps(articles, indent=4, ensure_ascii=False))
    #
    # with open(f"{filename.split('.')[0]}.json", "w") as json_file:
    #     json_file.write(json.dumps(articles, indent=4, ensure_ascii=False))
