"""library to print nicely formatted objects
"""


def content_summary(packets_summary):
    """print packets summary list"""
    print("=== CONTENT SUMMARY ===")
    for key, values in packets_summary.items():
        print("TYPE:", key, "\tAMOUNT:", values[0], "\tMEAN LENGTH:",
              round(values[1]/values[0], 0), "\tFIRST TS:", values[2],
              "\tLAST TS:", values[3])


def ip_addr_summary(ip_summary):
    """print ip summary table"""
    print("\n=== IP SUMMARY TABLE ===")
    for key, value in sorted(ip_summary.items(),
                             key=lambda x: x[1], reverse=True):
        sent, recv = str(value[0]), str(value[1])
        print("IP: {:15s}\tSENT: {:4s}\tRECV: {:4s}".format(key, sent, recv))


def urls_and_files(set_of_emails, set_of_urls, set_of_images):
    """print urls and file names"""
    print("\n=== EMAIL ADDRESSES ===")
    for email in set_of_emails:
        print(email)
    max_length = len(max(set_of_urls, key=len))
    print("\n=== URLS AND FILE NAMES ===")
    for num, url in enumerate(set_of_urls):
        print(f"PATH: {url:{max_length}s}\tNAME: {set_of_images[num]}")
