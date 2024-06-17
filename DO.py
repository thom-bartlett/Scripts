
import os
import boto3
import botocore
import sys

def main():
    hostname = sys.argv[1]
    print (hostname)
    # sf_path = "/Users/tbartlett/Downloads/"
    # ssl_path = "/Users/tbartlett/Downloads/"
    ssl_path = "/etc/nginx/vhosts/ssl_venturewell.org/"
    files = ["venturewell.org.fullchain", "venturewell.org.key", "sf-auth.venturewell.org.htpasswd"]
    session = boto3.session.Session()
    client = session.client('s3',
                            config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                            region_name='nyc3',
                            endpoint_url='https://nyc3.digitaloceanspaces.com',
                            aws_access_key_id="DO008BZ8KY3PWKQ4UZDK",
                            aws_secret_access_key="XZUYDF2d2vneoKDsUF8pa1xMm/eKShQ1/BcSKtu06jg")
    for i in files:
        client.download_file('ulysses-test',
                            i,
                            ssl_path+i,)
    os.rename("/etc/nginx/vhosts/ssl_venturewell.org/sf-auth.venturewell.org.htpasswd", f"/etc/nginx/vhosts/{hostname}.venturewell.org.htpasswd")

main()