package com.onearth.floodwatch;
/**
 * Copyright 2016 IBM Corp. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF Am    NY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteStatement;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.cloudant.sync.datastore.Datastore;
import com.cloudant.sync.datastore.DatastoreException;
import com.cloudant.sync.datastore.DatastoreManager;
import com.cloudant.sync.datastore.DocumentBodyFactory;
import com.cloudant.sync.datastore.DocumentException;
import com.cloudant.sync.datastore.DocumentRevision;
import com.cloudant.sync.datastore.UnsavedFileAttachment;
import com.ibm.mobilefirstplatform.clientsdk.android.core.api.BMSClient;
import com.ibm.mobilefirstplatform.clientsdk.android.core.api.Response;
import com.ibm.mobilefirstplatform.clientsdk.android.core.api.ResponseListener;
import com.ibm.mobilefirstplatform.clientsdk.android.core.api.Request;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.UnknownHostException;
import java.util.HashMap;
import java.util.Map;

/**
 * Main Activity implements Response listener for http request call back handling.
 */
public class MainActivity extends Activity implements View.OnClickListener, View.OnKeyListener{
    EditText usernameField;
    EditText passwordField;
    TextView changeSignUpModeTextView;
    TextView signUpButton;
    SQLiteDatabase myDatabase;
    Cursor c;

    Boolean signUpModeActive;


    private static final String TAG = MainActivity.class.getSimpleName();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        while(c != null){
            redirectUser();
        }
        signUpModeActive = true;

        usernameField = (EditText) findViewById(R.id.username);
        passwordField = (EditText) findViewById(R.id.password);
        changeSignUpModeTextView = (TextView) findViewById(R.id.changeSignUpMode);
        signUpButton = (TextView) findViewById(R.id.signUpButton);

        changeSignUpModeTextView.setOnClickListener(this);

//        try {
//            //initialize SDK with IBM Bluemix application ID and route
//            // You can find your backendRoute and backendGUID in the Mobile Options section on top of your Bluemix MCA dashboard
//            //TODO: Please replace <APPLICATION_ROUTE> with a valid ApplicationRoute and <APPLICATION_ID> with a valid ApplicationId
//            BMSClient.getInstance().initialize(this, "http://floodwatch.mybluemix.net", "：\n" +
//                    "005f7cca-f6cd-4c76-977a-80da3bbacb57", BMSClient.REGION_US_SOUTH);
//        }
//        catch (Exception e) {
//            signUpButton.setClickable(false);
//        }
    }

    public void redirectUser(){
        Intent i = new Intent(getApplicationContext(), MapsActivity.class);
        startActivity(i);
    }

    @Override
    public boolean onKey(View v, int keyCode, KeyEvent event) {


        if (keyCode == KeyEvent.KEYCODE_ENTER && event.getAction() == KeyEvent.ACTION_DOWN) {

            signUpOrLogIn(v);

        }

        return false;

    }
    @Override
    public void onClick(View v) {

        if (v.getId() == R.id.changeSignUpMode) {

            if (signUpModeActive == true) {
                signUpModeActive = false;
                changeSignUpModeTextView.setText("Sign Up");
                signUpButton.setText("Log In");
            } else {
                signUpModeActive = true;
                changeSignUpModeTextView.setText("Log In");
                signUpButton.setText("Sign Up");
            }
        } else if (v.getId() == R.id.top_text || v.getId() == R.id.bottom_text ||v.getId() == R.id.relativeLayout ){
            InputMethodManager imm = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);
            imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), 0);
        }

    }

    public void signUpOrLogIn(View view) {
        try {
            myDatabase = this.openOrCreateDatabase("Users", MODE_PRIVATE, null);
            myDatabase.execSQL("CREATE TABLE IF NOT EXISTS users (username VARCHAR, password VARCHAR, id INTEGER PRIMARY KEY)");

            if (signUpModeActive == true) {
                String sql = "INSERT INTO users (username, password) VALUES (?,?)";
                SQLiteStatement statement = myDatabase.compileStatement(sql);;
                statement.bindString(1, String.valueOf(usernameField.getText()));
                statement.bindString(2, String.valueOf(passwordField.getText()));
                statement.executeInsert();
                redirectUser();
                Toast.makeText(getApplicationContext(), "Sign Up Successful", Toast.LENGTH_SHORT).show();

            } else {
                c = myDatabase.rawQuery("SELECT * FROM Users", null);
                int nameIndex = c.getColumnIndex("username");
                int pwdIndex = c.getColumnIndex("password");
                int idIndex = c.getColumnIndex("id");
                c.moveToFirst();
                while (c != null) {
                    if (c.getString(nameIndex).equals(String.valueOf(usernameField.getText())) &&
                            c.getString(pwdIndex).equals(String.valueOf(passwordField.getText()))){
                        Toast.makeText(getApplicationContext(), "Login Successful", Toast.LENGTH_SHORT).show();
                        redirectUser();
                    }
                    c.moveToNext();
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }




    }


}
