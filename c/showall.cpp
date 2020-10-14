#include <iostream>
#include <vector>
#include <string>
#include <stdio.h>
#include <stdlib.h>

#include <cgicc/CgiDefs.h>
#include <cgicc/Cgicc.h>
#include <cgicc/HTTPHTMLHeader.h>
#include <cgicc/HTMLClasses.h>

#include "mysql_connection.h"

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
#include <cppconn/prepared_statement.h>

#define EXAMPLE_HOST "localhost"
#define EXAMPLE_USER "web_user"
#define EXAMPLE_PASS "mysqlroot"

using namespace std;
using namespace cgicc;

//http://ce.sharif.edu/courses/94-95/1/ce244-2/resources/root/cpp_web_programming.pdf
//https://www.tutorialspoint.com/cplusplus/cpp_web_programming.htm
// g++ -o getform.cgi getform.cpp -lcgicc -lmysqlcppconn; mv *.cgi /var/www/cgi-btn/
/*
 https://github.com/cmakified/cgicc/blob/master/demo/test.cpp
 https://www.gnu.org/software/cgicc/doc/cgicc_tutorial.html
 */
int main()
{
	Cgicc formData;
	bool math_flag, physics_flag;

	cout << "Content-type:text/html\r\n\r\n";
	cout << "<html>\n<head>\n";
	cout << "<title>C++ Form Get and Post Methods</title>\n";
	cout << "<link rel='stylesheet' href='/public/css/bootstrap_v3.3.7.min.css'>\n";
	cout << "<link rel='stylesheet' href='/public/css/google.Monsterrant.400.400.css'>\n";     
	cout << "<link rel='stylesheet' href='/public/css/font-awesome.v4.6.3.min.css'>\n";
    cout << "<link rel='stylesheet' href='/public/css/styles.css'>\n";
    cout << "<script src='/public/js/jquery_v1.12.4.min.js'></script>\n";
    cout << "<script src='/public/js/bootstrap_v3.3.7.min.js'></script>\n";
	cout << "</head><body>\n" << endl;

	cout << "<div id='hero-image'><h1 id='hero-title'>Games App CGI C++</h1></div>\n";
	try {

  		sql::Driver *driver;
	  	sql::Connection *con;
  		sql::Statement *stmt;
	  	sql::ResultSet *res;
		sql::PreparedStatement *pstmt;

		driver = get_driver_instance();
		con = driver->connect("tcp://127.0.0.1:3306", "web_user", "mysqlroot");
	
		con->setSchema("games");

		form_iterator game_id = formData.getElement("gid");
		cout << "<h1>" << **game_id << "</h1>";
		if(!game_id->isEmpty())
		{
			pstmt = con->prepareStatement("select id,console_name,console_shortname,coalesce(twitter,'') as twitter,coalesce(facebook,'') as facebook "
		"from games.game_console where id= ?;");
			int gid = (*game_id).getIntegerValue();
			printf("test me %d",gid);
			
			pstmt->setInt(1,gid);
			res = pstmt->executeQuery();
			while (res->next())
			{
				cout << res->getString("console_name");
			}
			//cout << "First Name is :" << **game_id ;		
			
			delete res;
			delete pstmt;
		}
		else
		{
			cout << "No first name was entered! :(";
		}
			
		pstmt = con->prepareStatement("select id,console_name,console_shortname,coalesce(twitter,'') as twitter,coalesce(facebook,'') as facebook "
		"from games.game_console;");
		res = pstmt->executeQuery();
						
		cout << "<nav class='navbar navbar-fixed-top'><div class='content-padding'>" << endl;
        cout << "<ul class='nav navbar-nav navbar-right'><li><a href='/cgi-bin/games.cgi'>Home</a></li>";
		cout << "<li class='dropdown'>";
		cout << "<a href'#' class='dropdown-toggle' data-toggle='dropdown'>Home <i class='fa fa-chevron-down'></i></a>";
		cout << "<ul class='dropdown-menu'>" << endl;
		while (res->next())
		{
			cout << "<li><a href ='/cgi-bin/console_games.cgi?cid="<< res->getInt("id")<<"' class='episode_link'>";
			cout << res->getString("console_shortname")<<"</a></li>" << endl;
		}
		cout <<"</ul></li></ul></div></nav>" << endl;	
    
		delete res;
		delete pstmt;
		
		pstmt = con->prepareStatement("select id,console_name,console_shortname,coalesce(twitter,'') as twitter,coalesce(facebook,'') as facebook from games.game_console;");
		res = pstmt->executeQuery();		

		cout << "<div id='posters-wrapper' class='content-padding clearfix'>";      
    				
		while (res->next())
		{
			cout << "<div class='poster-consoles'><a href='showall.cgi?gid=" << res->getInt("id") <<"'>";
		    cout << "<img src='/public/images/" << res->getString("console_shortname") << "/";
		    cout << res->getString("console_shortname")<<".png' "; 
		    cout << "alt='"<< res->getString("console_name")<<"' class='img-responsive'/>";
		    cout << "<div class='poster-consoles-info-overlay'><h3>" << res->getString("console_shortname") << "</h3>";
			cout << "<h4>View more <i class='fa fa-arrow-right'></i></h4></div></a></div>";
		}
		cout << "</div>" << endl;
		delete res; 
		delete pstmt;
		
		con->close();
		delete con;

	} catch (sql::SQLException &e) {
    	/*
      	MySQL Connector/C++ throws three different exceptions:
      - sql::MethodNotImplementedException (derived from sql::SQLException)
      - sql::InvalidArgumentException (derived from sql::SQLException)
      - sql::SQLException (derived from std::runtime_error)
    	*/
    	cout << "# ERR: SQLException in " << __FILE__;
    	cout << "(" << __FUNCTION__ << ") on line " << __LINE__ << endl;
    	/* what() (derived from std::runtime_error) fetches error message */
    	cout << "# ERR: " << e.what();
    	cout << " (MySQL error code: " << e.getErrorCode();
    	cout << ", SQLState: " << e.getSQLState() << " )" << endl;

    	return EXIT_FAILURE;
  	}
    cout << "<footer><div class='content-padding'>";
    cout << "<div class='footer-content'>";
	cout << "<p>Copyright &copy; Game Consoles Application &nbsp;</p>";
	cout << "<p><a href='/'>Main</a></p><div class='social-media-icons'></div>";
	cout << "</div></div></footer>" << endl;
    
	cout << "</body></html>\n";
	return 0;
}
