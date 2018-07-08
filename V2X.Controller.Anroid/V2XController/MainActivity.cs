using Android.App;
using Android.Widget;
using Android.OS;
using Android.Support.V7.App;
using Android.Hardware;
using System;
using System.Text;
using Android.Content.PM;
using Android.Views;
using RasPiBtControl.Droid.Services;

namespace RaspRCTruckOrginal
{
    [Activity(Label = "@string/app_name", Theme = "@style/AppTheme", MainLauncher = true, ScreenOrientation = ScreenOrientation.Landscape)]
    public class MainActivity : AppCompatActivity
    {
        Button btnStop;
        Button btnStart;
        Button btnLeft;
        Button btnRight;
        Button btnSlow;
        Button btnFast;
        string macAddressOfPi = "B8:27:EB:AC:7E:16";
        BtClient _btClient;
        public MainActivity()
        {
            try
            {
                _btClient = new BtClient();
                _btClient.Connect(macAddressOfPi);
            }
            catch(Exception ex)
            {
                Toast.MakeText(this, "Bluetooth Connection error", ToastLength.Long).Show();
            }
            //RequestWindowFeature(WindowFeatures.NoTitle);
            //Remove notification bar
            //Window.SetFlags(WindowManagerFlags.Fullscreen, WindowManagerFlags.Fullscreen);
        }

        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.activity_main);

            btnStart = FindViewById<Button>(Resource.Id.btnStart);
            btnStart.Click += btnStart_OnClick;
            btnStop = FindViewById<Button>(Resource.Id.btnStop);
            btnStop.Visibility = ViewStates.Invisible;
            btnStop.Click += btnStop_OnClick;

            btnLeft = FindViewById<Button>(Resource.Id.btnLeft);
            btnLeft.Click += btnLeft_OnClick;

            btnRight = FindViewById<Button>(Resource.Id.btnRight);
            btnRight.Click += btnRight_OnClick;

            btnFast = FindViewById<Button>(Resource.Id.btnFaster);
            btnFast.Click += btnFast_OnClick;

            btnSlow = FindViewById<Button>(Resource.Id.btnSlow);
            btnSlow.Click += btnSlow_OnClick;


        }

        private void btnSlow_OnClick(object sender, EventArgs e)
        {
            _btClient.SendData("Decelerate");
        }

        private void btnFast_OnClick(object sender, EventArgs e)
        {
            _btClient.SendData("Accelerate");
        }

        private void btnRight_OnClick(object sender, EventArgs e)
        {
            _btClient.SendData("Right");
        }

        private void btnLeft_OnClick(object sender, EventArgs e)
        {
            _btClient.SendData("Left");
        }

        public void btnStart_OnClick(object sender, EventArgs args)
        {
            btnStop.Visibility = ViewStates.Visible;
            btnStart.Visibility = ViewStates.Invisible;
            _btClient.SendData("Start");
            Toast.MakeText(this, "Hello from Start", ToastLength.Long).Show();
        }
        public void btnStop_OnClick(object sender, EventArgs args)
        {
            btnStop.Visibility = ViewStates.Invisible;
            btnStart.Visibility = ViewStates.Visible;
            _btClient.SendData("Stop");
            Toast.MakeText(this, "Hello from Stop", ToastLength.Long).Show();
        }

        protected override void OnResume()
        {
            base.OnResume();
        }

        protected override void OnPause()
        {
            base.OnPause();
        }
    }
}

