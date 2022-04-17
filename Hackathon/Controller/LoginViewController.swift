//
//  LoginViewController.swift
//  Hackathon
//
//  Created by Tony Razo on 4/16/22.
//

import UIKit
import Parse

class LoginViewController: UIViewController {
    
    
    @IBOutlet weak var usernameLabel: UITextField!
    @IBOutlet weak var passwordLabel: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    @IBAction func onSignIn(_ sender: Any) {
        let username = usernameLabel.text!
                let password = passwordLabel.text!
                
                PFUser.logInWithUsername(inBackground: username, password: password) { user, Error in
                    if user != nil {
                        self.performSegue(withIdentifier: "loginSegue", sender: nil)
                    }
                    else {
                        print("Error: \(Error?.localizedDescription)")
                    }
                }
    }
    
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
