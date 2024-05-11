from speedtest.speedtest import Speedtest

def test_network_speed():
    st = Speedtest()
    st.get_best_server()

    download_speed = st.download() / 1024 / 1024  # в мегабитах в секунду
    upload_speed = st.upload() / 1024 / 1024  # в мегабитах в секунду

    return download_speed, upload_speed

def main():
    download_speed, upload_speed = test_network_speed()
    print(f"Скорость загрузки: {download_speed:.2f} Мбит/с")
    print(f"Скорость выгрузки: {upload_speed:.2f} Мбит/с")

if __name__ == "__main__":
    main()
