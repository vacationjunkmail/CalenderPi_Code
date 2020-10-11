#include <iostream>
#include <vector>
#include <string>
#include <stdio.h>
#include <stdlib.h>

#include <string>
#include <cgicc/CgiDefs.h>
#include <cgicc/Cgicc.h>
#include <cgicc/HTTPHTMLHeader.h>
#include <cgicc/HTMLClasses.h>

#include "mysql_connection.h"

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>

#define EXAMPLE_HOST "localhost"
#define EXAMPLE_USER "web_user"
#define EXAMPLE_PASS "mysqlroot"

using namespace std;
using namespace cgicc;

//http://ce.sharif.edu/courses/94-95/1/ce244-2/resources/root/cpp_web_programming.pdf
//https://www.tutorialspoint.com/cplusplus/cpp_web_programming.htm
// g++ -o getform.cgi getform.cpp -lcgicc -lmysqlcppcon; mv *.cgi /var/www/cgi-btn/
const string ENV[ 24 ] = {
"COMSPEC", "DOCUMENT_ROOT", "GATEWAY_INTERFACE",
"HTTP_ACCEPT", "HTTP_ACCEPT_ENCODING",
"HTTP_ACCEPT_LANGUAGE", "HTTP_CONNECTION",
"HTTP_HOST", "HTTP_USER_AGENT", "PATH",
"QUERY_STRING", "REMOTE_ADDR", "REMOTE_PORT",
"REQUEST_METHOD", "REQUEST_URI", "SCRIPT_FILENAME",
"SCRIPT_NAME", "SERVER_ADDR", "SERVER_ADMIN",
"SERVER_NAME","SERVER_PORT","SERVER_PROTOCOL",
"SERVER_SIGNATURE","SERVER_SOFTWARE" };

int main()
{
	Cgicc formData;
	bool math_flag, physics_flag;

	cout << "Content-type:text/html\r\n\r\n";
	cout << "<html>\n<head>\n";
	cout << "<title>C++ Form Get and Post Methods</title>\n";
	cout << "<link rel='stylesheet' href='/public/css/bootstrap_v3.3.7.min.css'></head>\n";
	cout << "<body>\n";

	cout << "<table class='table table-sm table-bordered'>\n<tr><td>";
	form_iterator fi = formData.getElement("first_name");
	if( !fi->isEmpty() && fi != (*formData).end() )
	{
		cout << "First Name is :" << **fi;		
	}
	else
	{
		cout << "No first name was entered! :(";
	}

	cout << "</td></tr>\n<tr><td>";

	//form_iterator ln = formData.getElement("last_name");
	fi = formData.getElement("last_name");
	if( !fi->isEmpty() && fi != (*formData).end() )
	{
		cout << "Last Name is :" << **fi;		
	}
	else
	{
		cout << "No last name was entered! :(";
	}

	cout << "</td></tr>" << endl;

	fi = formData.getElement("subject");
	
	cout << "<tr><td>Radio Box: ";

	if ( !fi->isEmpty() && fi != (*formData).end() )
	{
		cout << **fi << endl;
	}
	else
	{
		cout << "No radio box data";
	}
	cout << "</td></tr>";

	math_flag = formData.queryCheckbox("maths");
	cout << "<tr><td>";
	if(math_flag){
		cout << "Math Check box Flag is on: " <<  endl;
	} else {
		cout << "Math Check box Flag is off: " << endl;
	}
	cout << math_flag << "</td></tr>";

	physics_flag = formData.queryCheckbox("physics");
	cout << "<tr><td>Physics Checkbox Flag is ";
	if(physics_flag){
		cout << "on: " <<  endl;
	} else {
		cout << "off: " << endl;
	}
	cout << physics_flag << "</td></tr>";
	
	cout << "<tr><td>Textarea content:<br />";
	fi = formData.getElement("textcontent");
	if( !fi->isEmpty() && fi != (*formData).end() ){
		cout << **fi << endl;
	} else{
		cout << "no content found!";
	}
	cout << "</td></tr>";

	fi = formData.getElement("dropdown");
	cout << "<tr><td>Dropdown value: ";
	if( !fi->isEmpty() && fi != (*formData).end()) {
		cout << **fi << endl;
	} else{
		cout << "No selection found!";
	}
	cout << "</td></tr>";
	cout << "</table>";

	fi = formData.getElement("dana");
	cout << "<font style='text-underline'>" << **fi << "</font>";

	try {

  		sql::Driver *driver;
	  	sql::Connection *con;
  		sql::Statement *stmt;
	  	sql::ResultSet *res;

		driver = get_driver_instance();
		con = driver->connect("tcp://127.0.0.1:3306", "web_user", "mysqlroot");
	
		con->setSchema("games");
		stmt = con->createStatement();
		res = stmt->executeQuery("select c.id as console_id,v.id,v.name,v.small_image,v.large_image from games.game_console as c "
		"inner join games.video_games as v on v.console_id = c.id where c.id=13 limit 5;");
		cout << "<table class='table table-bordered table-striped'>\n";
		while (res->next())
		{
			cout << "<tr><td>" << res->getInt("id") << "</td><td>" << res->getString("name") << "</td>" << endl;
			cout << "<td><img src='/public/images/PS4/small/" << res->getString("small_image") << "'></td></tr>";
			//also can be referenced by position.  res->getString(1)
		}
		cout << "</table>\n";
		delete res;
		delete stmt;
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

	cout << "<br />\n\n\n<table class='table table-striped table-bordered table-hover'>\n";

	for ( int i = 0; i < 24; i++ )
	{
		cout << "<tr><td>" << ENV[i] << "</td><td>";
		char *value = getenv(ENV[i].c_str());
		if(value !=0)
		{
			cout << value;
		}
		else
		{
			cout << "Environment variable does not exist.";
		}
		cout << "</td></tr>";
	}

	cout << "</table></body></html>\n";
	return 0;
}
