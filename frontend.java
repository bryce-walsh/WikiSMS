import java.io.IOException;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.twilio.twiml.messaging.Body;
import com.twilio.twiml.messaging.Message;
import com.twilio.twiml.MessagingResponse;
import com.twilio.twiml.TwiMLException;

public class TwilioServlet extends HttpServlet {
  public void service(HttpServletRequest request, HttpServletResponse response) throws IOException {
  	Sting body = request.getParameter("Body");
  	if(body.charAt(0) == '*'){
  		//message = getDesiredSearch(body.substring(1,body.length())) function the takes in
      // infobox keywords and returns a string for the keyword that the user desires
  		Body messageBody = new Body.Builder(message).build();
  		Message sms = new Message.Builder().body(messageBody).build();
  		MessagingResponse twiml = new MessagingResponse.Builder.message(sms).build();
  		response.setContentType("application/xml");

  		try {
  			response.getWriter().print(twiml.toXml());
  		} catch(TwiMLException e){
  			e.printStackTrace();
  		}
  	}

  	else{
  		//displayresults(body) function to display the query results to the user
  	}
