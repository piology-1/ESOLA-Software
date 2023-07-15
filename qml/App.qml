import QtQuick 2.15

AppScreen {
    id: root

    BackendBridge {
       id: mockBackendBridge
    }
    // Wird von Python aus zur Laufzeit mit "echter" BackendBridge ersetzt
    property QtObject backendBridge: mockBackendBridge

    property string batteryType
    property int compartmentIndex


    property string admin_card_uid
    property string new_user_card_uid
    property string user_card_uid_to_delete
    property string new_admin_card_uid
    property string admin_card_uid_to_delete

    property string global_previousState_ManagementMenu
    property string global_previousState_Compartments // to save the state, wheter ist "einlagern" or "entnehmen"

    Timer {
        id: finishScreenTimer
        interval: Constants.finishScreenDuration
        onTriggered: function() {
            root.state = "home"
        }
    }

    Timer {
        id: standbyTimer
        running: true
        interval: Constants.standbyTimeout
        onTriggered: function() {
            topBar.helpOverlay.state = "collapsed"
            root.state = "welcome"
        }
    }

    property var backFrom: {
        "batterytype": function() {
            root.state = "home"
        },
        "compartment": function() {
            root.state = "batterytype"
        },
        "authorizeRFID": function() {
            root.state = "compartment"
        },
        "managementMenu": function() {
            root.state = "home"
        }
    }

    topBar.button_x.onClicked: function(mouse) {
        if (root.state == "home"){
            root.state = "welcome"
        } else {
            root.state = "home"
        }
        userManagement.state = "base state"

    }

    button_back.onClicked: function(mouse) {
        backFrom[root.state]()
    }

    welcomeScreen.onClicked: function(mouse) {
        root.state = "home"
    }

    error_caseForm.onCancel: function(mouse){
        root.state = "home"
    }
    error_caseForm.onRetry: function(mouse){
        root.state = "authorizeRFID"
    }

    finishScreen.onClicked: function(mouse){
        root.state = "home"
    }

    finishScreen.onCancel: function(mouse){
        root.state = "home"
    }

    finishScreen.onRetry: function(mouse){
        root.state = "authorizeRFID"
    }



    homeScreen.einlagern.onClicked: function(mouse) {
        root.state = "batterytype";
        batteryTypeScreen.state = "deposit"
        compartmentScreen.state = "deposit"
        authorizeScreen.state = "deposit"
        authorizeScreen_RFID.state = "deposit"
        finishScreen.state = "deposit"

        // This variable is used to show the correct screen when a card does not exist in the system. 
        // The variable is also used to set the global state of compartments to "deposit".
        global_previousState_Compartments = "deposit"
    }
    homeScreen.entnehmen.onClicked: function(mouse) {
        root.state = "batterytype"
        batteryTypeScreen.state = "retrieve"
        compartmentScreen.state = "retrieve"
        authorizeScreen.state = "retrieve"
        authorizeScreen_RFID.state = "retrieve"
        finishScreen.state = "retrieve"

        // This variable is used to show the correct screen when a card is not authorized to unlock the door. Only the card that was used to lock the door is authorized for unlocking the door.
        // The variable is also used to set the global state of compartments to "retrieve".
        global_previousState_Compartments = "retrieve"
    }

    homeScreen.registrieren.onClicked: function(mouse) {
        root.state = "managementMenu"
    }


    batteryTypeScreen.bosch.onClicked: function(mouse) {
        onBatteryTypeSelected("bosch")
    }
    batteryTypeScreen.panasonic.onClicked: function(mouse) {
        onBatteryTypeSelected("panasonic")
    }
    batteryTypeScreen.panterra.onClicked: function(mouse) {
        onBatteryTypeSelected("panterra")
    }
    function onBatteryTypeSelected(type) {
        batteryType = type
        maskCompartments(batteryTypeScreen.state)
        root.state = "compartment"
    }

    // Belegte Fächer abfragen und Buttons im CompartmentScreen entsprechend ausgrauen.
    // Bei Einlagern außerdem in occupied-State versetzen, wenn alle belegt.
    function maskCompartments(state) {
        let enableMask = state === "deposit" ? backendBridge.getAvailableComps(batteryType) : backendBridge.getOccupiedComps(batteryType)
        let allOccupied = state === "deposit"
        compartmentScreen.buttons.forEach(b => {
            b.state = "disabled"
            b.visible = false
        })
        for (let i = 0; i < Math.min(enableMask.length, compartmentScreen.buttons.length); i++)  {
            compartmentScreen.buttons[i].visible = true
            if (enableMask[i]) {
                allOccupied = false
                compartmentScreen.buttons[i].state = ""
            }
        }
        compartmentScreen.state = allOccupied ? "occupied" : state
    }

    compartmentScreen.onCompartmentSelected: function(number) {
        compartmentIndex = number - 1
        root.state = "authorizeRFID"
    }

    authorizeScreen.onPinConfirmed: function(pin) {
        var funcByState = {
            "deposit": backendBridge.pinLock,
            "retrieve": backendBridge.pinUnlock
        }
        if(funcByState[authorizeScreen.state](batteryType, compartmentIndex, pin)) {
            root.state = "finish"
            finishScreenTimer.start()
        } else {
            authorizeScreen.wrongPinAnimation.running = true
            authorizeScreen.pinPad.confirmable = false
        }
    }



    userManagement.onCancel: function(mouse){
        root.state = "home"
        userManagement.state = "base state"
    }


    
    managementMenu.loeschenAdmin.onClicked: function(mouse) {
        menuModeSelected("loeschenAdmin")
    }
    managementMenu.registerAdmin.onClicked: function(mouse) {
        menuModeSelected("registerAdmin")
    }
    managementMenu.loeschenUser.onClicked: function(mouse) {
        menuModeSelected("loeschenUser")
    }
    managementMenu.registerUser.onClicked: function(mouse) {
        menuModeSelected("registerUser")
    }

    function menuModeSelected(previous_state){
        root.state = "userManagement"
        userManagement.state = "authorize_admin"
        global_previousState_ManagementMenu = previous_state
    }



    authorizeScreen_RFID.onScanConfirmed: function () {
        if (!backendBridge.reader_is_available()) {
            // set GUI screen to reader_not_available-screen
            error_caseForm.state = "NoCardReader"
            root.state = "errorcase"
            return // exit the function
        }
        // else, reader is available and ready to scan the RFID card

        // scan the smartcard on button press and set instance variables like card UID, if successful or Error message if failed
        backendBridge.scan_card()

        var funcByStateDoor = {
            "deposit": backendBridge.rfidLock,
            "retrieve": backendBridge.rfidUnlock
        }

        // can be deleted after varification, that it works with funcByStateNextState...
        // var funcByStateNextState = {
        //     // show the right screen, the card does not exist when a user tries to deposit an akku
        //     "deposit": function(){
        //         userManagement.state = "does_not_exists"
        //     },
        //     // Display the "noPermission" screen when the UID of the deposited card does not match the expected card's UID
        //     "retrieve": function(){
        //         finishScreen.state = "permission_denied"
        //     }
        // }
        

        if (backendBridge.get_reading_status()){
            // card could be read successfully
            var card_uid = backendBridge.get_card_uid()

            // check, whether the scanned card UID matches any entries in the all users database, but ONLY if the user wants to deposit an akku
            if (!backendBridge.user_exists_in_all_users_db(card_uid) && global_previousState_Compartments == "deposit") {
                // the read card UID does not exist in the all users database yet.
                root.state = "userManagement"
                userManagement.state = "does_not_exists"
                // funcByStateNextState[global_previousState_Compartments]()
            }
            else {
                // the scanned card UID exists in the all users database and is therefore a valid user for the ESOLA!

                var old_mode = batteryTypeScreen.state // to get to the right screen, if a right card was inserted after a wrong
                // card was inserted and the user pressend "try again"
                if(funcByStateDoor[authorizeScreen_RFID.state](batteryType, compartmentIndex, card_uid)) {
                    // if card was successfully read, set GUI to finishScreen
                    root.state = "finish"
                    finishScreen.state = old_mode
                    finishScreenTimer.start()
                } else {
                    root.state = "finish"
                    finishScreen.state = "permission_denied"
                    // funcByStateNextState[global_previousState_Compartments]()
                }
            }
        }
        else {
            root.state = "errorcase"
            // set the error case state regarding the returned error message
            error_caseForm.state = backendBridge.get_error_message()
        }
    }



    userManagement.onScan_admin: function(mouse){
        admin_card_uid = "" // reset to default admin_card_uid
        if (!backendBridge.reader_is_available()) {
            // set GUI screen to reader_not_available-screen
            error_caseForm.state = "NoCardReader"
            root.state = "errorcase"
            return // exit the function
        }

        var funcByState = {
            "loeschenAdmin": function(){
                userManagement.state = "delete_admin"
            }    ,
            "registerAdmin": function(){
                userManagement.state = "authorize_new_admin"
            }    ,
            "loeschenUser": function(){
                userManagement.state = "delete_user"
            }    ,
            "registerUser": function(){
                userManagement.state = "authorize_new_user"
            }
        }
        
        backendBridge.scan_card()

        if (backendBridge.get_reading_status()){
            // card could be read successfully
            admin_card_uid = backendBridge.get_card_uid()

            if (!backendBridge.admin_exists_in_admin_db(admin_card_uid)) {
                // given/ scanned card is not a valid admin smartcard
                userManagement.state = "InvalidAdminCard"
                return
            }
            else {
                // given/ scanned card is a valid admin smartcard
                print(global_previousState_ManagementMenu)
                // --> passt. Hat jeweils den Wert auf den es in der onFoo() function oben gesetzt wurde
                // (loeschenAdmin, registerAdmin, loeschenUser, registerUser)
                funcByState[global_previousState_ManagementMenu]()
            }
        } else {
            root.state = "errorcase"
            error_caseForm.state = backendBridge.get_error_message()
        }

    }


    /// ADD CODE \\\
    userManagement.onScan_new_user: function(mouse){
        new_user_card_uid = "" // reset to default new_user_card_uid
        if (!backendBridge.reader_is_available()) {
            // set GUI screen to reader_not_available-screen
            error_caseForm.state = "NoCardReader"
            root.state = "errorcase"
            return // exit the function
        }

        backendBridge.scan_card()

        if (backendBridge.get_reading_status()){
            // card could be read successfully
            new_user_card_uid = backendBridge.get_card_uid()

            if (backendBridge.user_exists_in_all_users_db(new_user_card_uid)) {
                userManagement.state = "already_exists"
                return
            }



            if (backendBridge.add_new_user_to_all_users_db(new_user_card_uid, admin_card_uid)){
                userManagement.state = "successfully_added"
            }
            else {
                userManagement.state = "unsuccessful_add"
            }
        } else {
            root.state = "errorcase"
            error_caseForm.state = backendBridge.get_error_message()
        }
    }


    userManagement.onScan_new_admin: function(mouse){
        new_admin_card_uid = "" // reset to default new_admin_card_uid
        if (!backendBridge.reader_is_available()) {
            // set GUI screen to reader_not_available-screen
            error_caseForm.state = "NoCardReader"
            root.state = "errorcase"
            return // exit the function
        }

        backendBridge.scan_card()

        if (backendBridge.get_reading_status()){
            new_admin_card_uid = backendBridge.get_card_uid()

            if (backendBridge.admin_exists_in_admin_db(new_admin_card_uid) ||
                backendBridge.user_exists_in_all_users_db(new_admin_card_uid)) {
                userManagement.state = "already_exists"
                return
            }

            // add admin to both databases: the admin DB as well as the all users DB!
            if (backendBridge.add_new_admin_uid(new_admin_card_uid, admin_card_uid)) { // && backendBridge.add_new_user_to_all_users_db(new_admin_card_uid, admin_card_uid)){
                userManagement.state = "successfully_added"
            }
            else {
                userManagement.state = "unsuccessful_add"
            }
        } else {
            root.state = "errorcase"
            error_caseForm.state = backendBridge.get_error_message()
        }
    }

   
    /// DELETION CODE \\\
    userManagement.onDelete_user: function(mouse){
        if (!backendBridge.reader_is_available()) {
            error_caseForm.state = "NoCardReader"
            root.state = "errorcase"
            return // exit the function
        }

        backendBridge.scan_card()

        if (backendBridge.get_reading_status()){
            user_card_uid_to_delete = backendBridge.get_card_uid()

            
            if (backendBridge.admin_exists_in_admin_db(user_card_uid_to_delete)) {
                // insterted card is an admin card and therefore needs to be deleted over the admin deletion Button
                userManagement.state = "unsuccessful_delete_admin_via_all_users"
                return
            }

            if (!backendBridge.user_exists_in_all_users_db(user_card_uid_to_delete)) {
                userManagement.state = "does_not_exists" // and therefore cannot be deleted
                return
            }

            if (backendBridge.delete_user_from_all_users_db(user_card_uid_to_delete, admin_card_uid)){
                userManagement.state = "successfully_deleted"
            }
            else {
                userManagement.state = "unsuccessful_delete"
            }
        } else {
            root.state = "errorcase"
            error_caseForm.state = backendBridge.get_error_message()
        }

    }


    userManagement.onDelete_admin: function(mouse){
        if (!backendBridge.reader_is_available()) {
            error_caseForm.state = "NoCardReader"
            root.state = "errorcase"
            return // exit the function
        }

        backendBridge.scan_card()

        if (backendBridge.get_reading_status()){
            admin_card_uid_to_delete = backendBridge.get_card_uid()

            if (!backendBridge.admin_exists_in_admin_db(admin_card_uid_to_delete) ||
                !backendBridge.user_exists_in_all_users_db(admin_card_uid_to_delete)) {
                userManagement.state = "does_not_exists"
                return
            }

            // delete admin from both databases: the admin DB as well as the all users DB!
            if (backendBridge.delete_admin_uid(admin_card_uid_to_delete, admin_card_uid)) { // && backendBridge.delete_user_from_all_users_db(admin_card_uid_to_delete, admin_card_uid)){
                userManagement.state = "successfully_deleted";
            }
            else {
                userManagement.state = "unsuccessful_delete"
            }
        } else {
            root.state = "errorcase"
            error_caseForm.state = backendBridge.get_error_message()
        }
    }


    standbyResetMouseArea.onPressed: function(mouse) {
        standbyTimer.restart()
        mouse.accepted = false
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:1.33;height:480;width:640}
}
##^##*/
