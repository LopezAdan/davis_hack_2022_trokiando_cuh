//
//  SignUpViewController.swift
//  Hackathon
//
//  Created by Tony Razo on 4/16/22.
//

import UIKit
import Parse

class SignUpViewController: UIViewController {

    @IBOutlet weak var userLabel: UITextField!
    @IBOutlet weak var passLabel: UITextField!
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }
    
    @IBAction func onSignUp(_ sender: Any) {
        let user = PFUser()
        user.username = userLabel.text!
        user.password = passLabel.text!

        user.signUpInBackground { success, error in
            if success {
                self.performSegue(withIdentifier: "singupSegue", sender: nil)
            }
            else {
                print("Error: \(error?.localizedDescription)")

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
