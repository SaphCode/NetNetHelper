GUIDE FOR CHROMEDRIVER ON SELENIUM:
https://stackoverflow.com/questions/18674092/how-to-implement-chromedriver-in-selenium-in-linux-platform

We have installed Successfully

sudo apt-get install unzip
wget -N http://chromedriver.storage.googleapis.com/2.10/chromedriver_linux64.zip -P ~/Downloads
unzip ~/Downloads/chromedriver_linux64.zip -d ~/Downloads
chmod +x ~/Downloads/chromedriver
sudo mv -f ~/Downloads/chromedriver /usr/local/share/chromedriver
Change the directory to /usr/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

Now run the script and add the following in the environment file.

Capybara.register_driver :chrome do |app| client = Selenium::WebDriver::Remote::Http::Default.new Capybara::Selenium::Driver.new(app, :browser => :chrome, :http_client => client) end

Capybara.javascript_driver = :chrome

Note : Change the chrome driver version according to your operating system type like 32 bit or 64 bit.
