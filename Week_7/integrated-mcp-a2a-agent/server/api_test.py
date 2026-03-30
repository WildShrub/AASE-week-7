import handlers

#print(handlers.get_github_issue(4))


#print(handlers.get_github_PR(2))

print(handlers.create_github_issue("test_Title", "I really hope this works"))


print(handlers.create_github_PR("test_pr_title", "test pr body", "test pr head", "base", True))


#print(handlers.git_diff("a2e7616daefe7f52ade93a083d8d5b0a12e18d7a~4","a2e7616daefe7f52ade93a083d8d5b0a12e18d7a"))


#print(handlers.placeholder())



