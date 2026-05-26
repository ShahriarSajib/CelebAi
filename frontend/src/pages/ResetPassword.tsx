import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

import axios from "axios";

import toast from "react-hot-toast";

import { Loader2 } from "lucide-react";

export default function ResetPassword() {

  const navigate = useNavigate();

  const [searchParams] = useSearchParams();

  const token = searchParams.get("token");

  const [newPassword, setNewPassword] = useState("");

  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const validatePassword = () => {

    if (newPassword.length < 6) {

      toast.error(
        "Password must be at least 6 characters"
      );

      return false;
    }

    if (newPassword !== confirmPassword) {

      toast.error(
        "Passwords do not match"
      );

      return false;
    }

    return true;
  };

  const handleReset = async () => {

    if (!validatePassword()) return;

    try {

      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/auth/reset-password",
        {
          token,
          new_password: newPassword,
        }
      );

      toast.success(response.data.message);

      setTimeout(() => {

        navigate("/login");

      }, 2000);

    } catch (error: any) {

      toast.error(
        error.response?.data?.detail ||
        "Something went wrong"
      );

    } finally {

      setLoading(false);
    }
  };

  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md">

        <h1 className="text-3xl font-bold mb-6 text-center">
          Reset Password
        </h1>

        <div className="space-y-4">

          <input
            type="password"
            placeholder="New Password"
            className="w-full border p-3 rounded-lg"
            value={newPassword}
            onChange={(e) =>
              setNewPassword(e.target.value)
            }
          />

          <input
            type="password"
            placeholder="Confirm Password"
            className="w-full border p-3 rounded-lg"
            value={confirmPassword}
            onChange={(e) =>
              setConfirmPassword(e.target.value)
            }
          />

          <button
            onClick={handleReset}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg flex justify-center items-center"
          >

            {loading ? (
              <Loader2 className="animate-spin" />
            ) : (
              "Reset Password"
            )}

          </button>

        </div>

      </div>

    </div>
  );
}