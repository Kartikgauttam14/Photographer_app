package com.photohire

import android.app.Application
import android.content.Context
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.firebase.FirebaseApp
import io.socket.client.IO
import io.socket.client.Socket
import java.net.URISyntaxException

class PhotoHireApp : Application() {
    private var socket: Socket? = null

    companion object {
        private const val SERVER_URL = "http://10.0.2.2:8000"  // Local development server
        private const val GOOGLE_WEB_CLIENT_ID = "your-web-client-id"  // Replace with your Google Web Client ID
        private lateinit var instance: PhotoHireApp

        fun getInstance(): PhotoHireApp = instance
        fun getSocket(): Socket? = instance.socket
    }

    override fun onCreate() {
        super.onCreate()
        instance = this

        // Initialize Firebase
        FirebaseApp.initializeApp(this)

        // Initialize Socket.IO
        setupSocketIO()

        // Initialize Google Sign In
        setupGoogleSignIn()
    }

    private fun setupSocketIO() {
        try {
            val options = IO.Options().apply {
                reconnection = true
                reconnectionDelay = 1000
                reconnectionDelayMax = 5000
            }
            socket = IO.socket(SERVER_URL, options)
        } catch (e: URISyntaxException) {
            e.printStackTrace()
        }
    }

    private fun setupGoogleSignIn() {
        val gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken(GOOGLE_WEB_CLIENT_ID)
            .requestEmail()
            .build()

        GoogleSignIn.getClient(this, gso)
    }

    override fun attachBaseContext(base: Context) {
        super.attachBaseContext(base)
    }

    override fun onTerminate() {
        super.onTerminate()
        socket?.disconnect()
        socket?.close()
    }
}