package com.wikisms.app.cdr;


import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.view.View;

// Install the Java helper library from twilio.com/docs/libraries/java
import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;

public class MainActivity extends AppCompatActivity {


    public static final String ACCOUNT_SID = "ACace136eec48e0b51b54ccadc38236267";
    public static final String AUTH_TOKEN = "f4a9b76b529979805290c0c8beb60771";
    public static final String TWILIO_NO = "+14703750399"; // From
    public static final String EMULATOR_NO = "+16505551212";  // To

    // These are the global variables
    EditText editSearch, editHint;
    TextView textResult;
    Button buttonSearch, buttonReset;
    String result = "";


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        editSearch = (EditText) findViewById(R.id.editSearch);
        editHint = (EditText) findViewById(R.id.editHint);
        textResult = (TextView) findViewById(R.id.textResult);
        buttonSearch = (Button) findViewById(R.id.buttonSearch);
        buttonReset = (Button) findViewById(R.id.buttonReset);


        /* Search Button */
        buttonSearch.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                // get text from EditText search view
                String search = editSearch.getText().toString();
                // get text from EditText hint view
                String hint = editHint.getText().toString();
                result = "Search term:\t" + search + "\nhint:\t" + hint;
                textResult.setText(result);
                sendMessage(result);

            }
        });

        /* Reset Button */
        buttonReset.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // clearing out all the values
                editSearch.setText("");
                editHint.setText("");
                textResult.setText("");
                editSearch.requestFocus();
            }
        });


    }

    //------------------sends an SMS message to another device---//
    public void sendMessage(String result) {

        Twilio.init(ACCOUNT_SID, AUTH_TOKEN);

        Message message = Message
                .creator(new PhoneNumber("+14703750399"), // to
                        new PhoneNumber("+12164100021"), // from
                        result)
                .create();

        System.out.println(message.getSid());
        System.out.print(result);
    }


}