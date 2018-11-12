import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;

public class FrontEnd{
	public static final String ACCOUNT_SID = "AC520affbaf6ae1ee496f05abfc2fba256";
	public static final String AUTH_TOKEN = "342cd21959401510580ee307c13b930e";

	public static void main(String[] args){
		send_sms("Working");
	}

	public static void send_sms(String body){
		Twilio.init(ACCOUNT_SID, AUTH_TOKEN);
		Message message = Message.creator(
				new com.twilio.type.PhoneNumber("+17706299609"),
				new com.twilio.type.PhoneNumber("+14703750399"),
				body).create();
	}
}
