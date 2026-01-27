import { X, User, Phone, CreditCard, Globe, Loader } from "lucide-react";
import { useState } from "react";

const languages = [
  { value: "en", label: "English (en)" },
  { value: "hi", label: "Hindi - हिंदी (hi)" },
  { value: "ta", label: "Tamil - தமிழ் (ta)" },
  { value: "te", label: "Telugu - తెలుგు (te)" },
  { value: "kn", label: "Kannada - ಕನ್ನಡ (kn)" },
  { value: "ml", label: "Malayalam - മലയാളം (ml)" },
  { value: "mr", label: "Marathi - मराठी (mr)" },
  { value: "gu", label: "Gujarati - ગુજરાતી (gu)" },
  { value: "bn", label: "Bengali - বাংলা (bn)" },
  { value: "or", label: "Odia - ଓଡ଼ିଆ (or)" },
  { value: "pa", label: "Punjabi - ਪੰਜਾਬੀ (pa)" },
  { value: "as", label: "Assamese - অসমীয়া (as)" },
  { value: "ur", label: "Urdu - اردو (ur)" },
  { value: "sa", label: "Sanskrit - संस्कृत (sa)" },
  { value: "mai", label: "Maithili - मैथिली (mai)" },
];

const ID_TYPES = [
  { value: "aadhar", label: "Aadhar Card", placeholder: "123456789012", format: "12 digits" },
  { value: "voter_id", label: "Voter ID", placeholder: "ABC1234567", format: "AAA1234567" },
  { value: "driving_license", label: "Driving License", placeholder: "DL2024123456", format: "SSYYYYNNNNNNN" },
  { value: "pan", label: "PAN Card", placeholder: "ABCDE1234F", format: "AAAAA1234A" },
];

const DriverHelperModal = ({ isOpen, onClose, type, onSave, loading }) => {
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    aadhar: "",
    idType: "aadhar",
    language: "en",
  });
  const [errors, setErrors] = useState({});

  if (!isOpen) return null;

  const formatPhoneValue = (value) => {
    const digits = value.replace(/\D/g, "");
    if (!digits) return "";
    const withoutCountry = digits.startsWith("91") ? digits.slice(2) : digits;
    const trimmed = withoutCountry.slice(0, 10);
    return trimmed ? `+91${trimmed}` : "";
  };

  const validateIdNumber = (idType, value) => {
    const cleaned = value.replace(/\s/g, "").replace(/-/g, "").toUpperCase();

    switch (idType) {
      case "aadhar":
        return /^\d{12}$/.test(cleaned) ? null : "Aadhar must be exactly 12 digits";
      case "voter_id":
        return /^[A-Z]{3}\d{7}$/.test(cleaned) ? null : "Voter ID must be AAA1234567 format";
      case "driving_license":
        return cleaned.length >= 13 && cleaned.length <= 16 ? null : "Driving License must be 13-16 characters";
      case "pan":
        return /^[A-Z]{5}\d{4}[A-Z]$/.test(cleaned) ? null : "PAN must be AAAAA1234A format";
      default:
        return null;
    }
  };

  const handleInputChange = (field, value) => {
    let nextValue = value;
    if (field === "phone") {
      nextValue = formatPhoneValue(value);
    }
    if (field === "aadhar") {
      const idType = formData.idType;
      // Format based on ID type
      if (idType === "aadhar") {
        nextValue = value.replace(/\D/g, "").slice(0, 12);
      } else if (idType === "voter_id") {
        nextValue = value.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 10);
      } else if (idType === "driving_license") {
        nextValue = value.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 16);
      } else if (idType === "pan") {
        nextValue = value.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 10);
      }
    }
    setFormData((prev) => ({ ...prev, [field]: nextValue }));
    setErrors((prev) => {
      const updated = { ...prev };
      delete updated[field];
      return updated;
    });
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.name.trim()) {
      newErrors.name = `${type} name is required`;
    }
    if (!formData.phone) {
      newErrors.phone = "Phone number is required";
    } else if (!/^\+91\d{10}$/.test(formData.phone)) {
      newErrors.phone = "Phone must follow +91XXXXXXXXXX format";
    }

    const idError = validateIdNumber(formData.idType, formData.aadhar);
    if (!formData.aadhar) {
      newErrors.aadhar = "ID number is required";
    } else if (idError) {
      newErrors.aadhar = idError;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validate()) {
      // Trim the aadhar before sending
      onSave({
        ...formData,
        aadhar: formData.aadhar.trim()
      });
      setFormData({ name: "", phone: "", aadhar: "", language: "en" });
      setErrors({});
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative z-10 w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900">
            Add New {type}
          </h2>
          <button
            onClick={onClose}
            className="rounded-lg p-2 hover:bg-gray-100 transition-colors"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {type} Name <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <User className="absolute left-3 top-3.5 h-5 w-5 text-gray-400 pointer-events-none" />
              <input
                type="text"
                value={formData.name}
                onChange={(e) => handleInputChange("name", e.target.value)}
                placeholder={`Enter ${type.toLowerCase()} name`}
                className={`w-full pl-10 pr-4 py-3 rounded-xl border text-sm font-medium transition-all ${errors.name
                  ? "border-red-400 bg-red-50"
                  : "border-gray-300 bg-white"
                  }`}
              />
            </div>
            {errors.name && (
              <p className="mt-1 text-sm text-red-600">{errors.name}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              ID Document Type <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <Globe className="absolute left-3 top-3.5 h-5 w-5 text-gray-400 pointer-events-none z-10" />
              <select
                value={formData.idType}
                onChange={(e) => {
                  handleInputChange("idType", e.target.value);
                  setFormData(prev => ({ ...prev, aadhar: "" })); // Clear ID number when type changes
                }}
                className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-300 bg-white text-sm font-medium appearance-none cursor-pointer"
              >
                {ID_TYPES.map((idType) => (
                  <option key={idType.value} value={idType.value}>
                    {idType.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Unique ID Number <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <CreditCard className="absolute left-3 top-3.5 h-5 w-5 text-gray-400 pointer-events-none" />
              <input
                type="text"
                inputMode={formData.idType === "aadhar" ? "numeric" : "text"}
                value={formData.aadhar}
                onChange={(e) => handleInputChange("aadhar", e.target.value)}
                placeholder={ID_TYPES.find(t => t.value === formData.idType)?.placeholder || "Enter ID number"}
                maxLength={formData.idType === "driving_license" ? 16 : formData.idType === "aadhar" ? 12 : 10}
                className={`w-full pl-10 pr-4 py-3 rounded-xl border text-sm font-medium transition-all ${errors.aadhar
                  ? "border-red-400 bg-red-50"
                  : "border-gray-300 bg-white"
                  }`}
              />
            </div>
            {errors.aadhar && (
              <p className="mt-1 text-sm text-red-600">{errors.aadhar}</p>
            )}
            <p className="mt-1 text-xs text-gray-500">
              Format: {ID_TYPES.find(t => t.value === formData.idType)?.format}
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Phone Number <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <Phone className="absolute left-3 top-3.5 h-5 w-5 text-gray-400 pointer-events-none" />
              <input
                type="tel"
                inputMode="numeric"
                value={formData.phone}
                onChange={(e) => handleInputChange("phone", e.target.value)}
                placeholder="+91XXXXXXXXXX"
                className={`w-full pl-10 pr-4 py-3 rounded-xl border text-sm font-medium transition-all ${errors.phone
                  ? "border-red-400 bg-red-50"
                  : "border-gray-300 bg-white"
                  }`}
              />
            </div>
            {errors.phone && (
              <p className="mt-1 text-sm text-red-600">{errors.phone}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Language <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <Globe className="absolute left-3 top-3.5 h-5 w-5 text-gray-400 pointer-events-none z-10" />
              <select
                value={formData.language}
                onChange={(e) => handleInputChange("language", e.target.value)}
                className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-300 bg-white text-sm font-medium appearance-none cursor-pointer"
              >
                {languages.map((lang) => (
                  <option key={lang.value} value={lang.value}>
                    {lang.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold py-3 rounded-xl transition-all flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader className="h-5 w-5 animate-spin" />
                Saving...
              </>
            ) : (
              <>
                <User className="h-5 w-5" />
                Save {type} Info
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DriverHelperModal;