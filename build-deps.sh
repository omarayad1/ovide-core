export PATH="$PATH:/app/vendor/bin"

wget http://garr.dl.sourceforge.net/project/flex/flex-2.5.39.tar.bz2 && tar -jxf flex-2.5.39.tar.bz2 && cd flex-2.5.39 && ./configure --prefix=/app/vendor && make && make install && cd ../
wget http://ftp.gnu.org/pub/gnu/gperf/gperf-3.0.4.tar.gz && tar -zxf gperf-3.0.4.tar.gz && cd gperf-3.0.4 && ./configure --prefix=/app/vendor && make && make install && cd ../
wget ftp://ftp.gnu.org/gnu/bison/bison-3.0.2.tar.gz && tar -zxf bison-3.0.2.tar.gz && cd bison-3.0.2 && ./configure --prefix=/app/vendor && make && make install && cd ../
wget ftp://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz && tar -zxf autoconf-2.69.tar.gz && cd autoconf-2.69 && ./configure --prefix=/app/vendor && make && make install && cd ../
wget ftp://icarus.com/pub/eda/verilog/snapshots/verilog-20141205.tar.gz && tar -zxf verilog-20141205.tar.gz && cd verilog-20141205 && ./configure --prefix=/app/vendor && make && make install && cd ../
wget http://www.veripool.org/ftp/verilator-3.866.tgz && tar -zxf verilator-3.866.tgz && cd verilator-3.866 && ./configure --prefix=/app/vendor && make && make install && cd ../
wget http://lftp.yar.ru/ftp/lftp-4.6.0.tar.gz && tar -zxf lftp-4.6.0.tar.gz && cd lftp-4.6.0 && ./configure --prefix=/app/vendor && make && make install && cd ../

wget ftp://$FTP_USERNAME:$FTP_PASSWORD@$FTP_HOST/ovide-static/upload_vendor.py
cd vendor
tar -czvf vendor.tar.gz bin include share lib

cd ../
mv vendor/vendor.tar.gz vendor.tar.gz
python upload_vendor.py vendor.tar.gz