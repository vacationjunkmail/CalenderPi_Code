#include <iostream>
using namespace std;

int main () {
   cout << "Content-type:text/html\r\n\r\n";
   cout << "<html><head>\n";
// cout << "<head>\n";
   cout << "<title>Hello World - First CGI Program</title>\n";
   cout << "<link rel='stylesheet' href='/public/css/bootstrap_v3.3.7.min.css'></head>\n";
   cout << "<body>\n";
   cout << "<div class='container'><h1>Hello World!</h1> <p class='lead'>This is C++ CGI program</h1></p>";
   cout << "</div></body>\n";
   cout << "</html>\n";
   
   return 0;
}
