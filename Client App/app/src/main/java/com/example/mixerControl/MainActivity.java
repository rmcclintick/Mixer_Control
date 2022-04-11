package com.example.mixerControl;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.SeekBar;
import android.widget.TextView;

import java.io.IOException;


public class MainActivity extends AppCompatActivity {

    public static final String EXTRA_MESSAGE = "com.example.myfirstapp.MESSAGE";
    //private SeekBar volumeBar;

    boolean socketOpen = false;
    UDPThread socket;
    String[] progNames;
    SeekBar[] faders;
    ConstraintLayout layout;
    LinearLayout linLay;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        layout = findViewById(R.id.mainLayout);
        linLay = findViewById(R.id.faderArea);



//        volumeBar = (SeekBar) findViewById(R.id.seekBar2);
//        volumeBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
//            @Override
//            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
//                try {
//                    setVolumeText(seekBar.getProgress() + "");
//                    socket.sendMessage(Integer.toString(seekBar.getProgress()));
//                } catch (IOException e) {
//                    e.printStackTrace();
//                }
//            }
//            @Override
//            public void onStartTrackingTouch(SeekBar seekBar) {}
//            @Override
//            public void onStopTrackingTouch(SeekBar seekBar) {}
//        });
        //Object[] objects = {this};
        //@SuppressLint("WrongThread") Object o = con.doInBackground(objects);
    }

    //called when user taps send button
    public void connectAndRefresh(View view)
    {
//        Intent intent = new Intent(this, DisplayMessageActivity.class);
//        EditText editText = (EditText) findViewById(R.id.editTextTextPersonName);
//        String message = editText.getText().toString();
//        intent.putExtra(EXTRA_MESSAGE, message);
//        startActivity(intent);
        try {

            EditText et = (EditText) findViewById(R.id.ipAddress);
            String address = et.getText().toString();
            if (!socketOpen)
            {
                createSocket(address);
                socketOpen = true;
            }
            else if (!address.equals(socket.getIP()))
            {
                createSocket(address);
            }
            socket.sendMessage("refresh");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void setVolumeText(String message) throws IOException {
        //TextView vt = findViewById(R.id.volumeText);
        //vt.setText(message);
        //con.dos.writeUTF(message);
        //System.out.println(s);
    }

    public void createSocket(String address)
    {
        try {
            socket= new UDPThread(address, this);
            socket.start();
        } catch(IOException e) {
            e.printStackTrace();
        }
    }

    public void createFaders(String[] names)
    {
        //System.out.println(names.toString());
        linLay.removeAllViews();
        faders = new SeekBar[names.length];
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        params.setMargins(8, 8, 8, 8);

        for (int j = 0; j < names.length; j++)
        {
            faders[j] = new SeekBar(this);
            faders[j].setLayoutParams(params);
            int finalJ = j;
            faders[j].setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                try {
                    //setVolumeText(seekBar.getProgress() + "");
                    socket.sendMessage(finalJ + " " + Integer.toString(seekBar.getProgress()));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {}
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {}
        });
            TextView label = new TextView(this);
            label.setText(names[j]);
            label.setLayoutParams(params);
            linLay.addView(label);

            linLay.addView(faders[j]);
        }
    }
}




