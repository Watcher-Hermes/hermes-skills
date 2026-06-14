# BAD: brittle class+index locator as primary strategy
page.by_class("Edit", index=2).type_keys("hello")