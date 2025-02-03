[Setup]
AppName=Scum Bard MIDI Player
AppVersion=1.0.0
AppPublisher=Plugin Project
AppPublisherURL=https://github.com/cooksta120021/Scum_Plug
AppSupportURL=https://github.com/cooksta120021/Scum_Plug/issues
AppUpdatesURL=https://github.com/cooksta120021/Scum_Plug/releases
DefaultDirName={pf}\ScumBard
DefaultGroupName=ScumBard
OutputBaseFilename=ScumBardInstaller
Compression=lzma2
SolidCompression=yes
SetupIconFile=scum_bard_icon.ico
UninstallDisplayIcon={app}\scum_bard.exe
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Types]
Name: "full"; Description: "Full installation"
Name: "compact"; Description: "Compact installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "main"; Description: "Main Application"; Types: full compact custom; Flags: fixed
Name: "data"; Description: "Sample MIDI Data"; Types: full

[Files]
Source: "..\dist\scum_bard.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: main
Source: "..\plugins\scum_bard\data\*"; DestDir: "{app}\data"; Flags: recursesubdirs createallsubdirs; Components: data
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion; Components: main
Source: "start.bat"; DestDir: "{app}"; Flags: ignoreversion; Components: main
Source: "stop.bat"; DestDir: "{app}"; Flags: ignoreversion; Components: main

[Icons]
Name: "{group}\Scum Bard MIDI Player"; Filename: "{app}\scum_bard.exe"; Components: main
Name: "{group}\Uninstall Scum Bard"; Filename: "{uninstallexe}"; Components: main
Name: "{commondesktop}\Scum Bard MIDI Player"; Filename: "{app}\scum_bard.exe"; Components: main

[Run]
Filename: "{app}\scum_bard.exe"; Description: "Launch Scum Bard"; Flags: postinstall nowait skipifsilent unchecked; Components: main

[UninstallRun]
Filename: "{app}\stop.bat"; Flags: runhidden

[UninstallDelete]
Type: files; Name: "{app}\scum_bard.exe"
Type: files; Name: "{app}\scum_bard.log"
Type: dirifempty; Name: "{app}"

[Code]
var
  FinishedInstall: Boolean;

function InitializeSetup(): Boolean;
begin
  // Add pre-installation checks here
  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then begin
    FinishedInstall := True;
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  // Add custom navigation logic if needed
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  // Add page change logic if needed
end;
