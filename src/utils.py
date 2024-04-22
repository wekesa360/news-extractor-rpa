from datetime import datetime


def take_screenshot_and_save_page_elements(browser_instance, element):
    try:
        browser_instance.screenshot(
            element, f"output/page_view_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        elements = browser_instance.find_elements("tag:*")
        output_file = "output/tags.txt"

        with open(output_file, "w") as f:
            for element in elements:
                tag_name = element.tag_name
                element_id = element.get_attribute("id")
                element_class = element.get_attribute("class")
                f.write(
                    f"Tag Name: {tag_name}\nID: {element_id}\nClass: {element_class}\n\n"
                )
        return True
    except Exception as e:
        print(f"Error viewing page elements: {str(e)}")
        return False
