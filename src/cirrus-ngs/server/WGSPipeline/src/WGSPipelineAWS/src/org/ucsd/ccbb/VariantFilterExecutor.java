package org.ucsd.ccbb;

import java.util.ArrayList;

/**
 * VariantFilterExecutor filters VCF variants using GATK VQSR.
 * 
 * @author Guorong Xu
 */
public class VariantFilterExecutor extends CommandExecutor {
	
	/**a string stores the shell script path*/
	public String m_shellScript = "";
	/**a string stores the file name*/
	public String m_fileName = "";
	/**a string stores the log path*/
	public String m_logFile = "";
	
	/**
	 * Assembles a shell command with specified shell script path, file name 
	 * and log path.
	 * The function overrides the assembleCommands from the class 
	 * CommandExecutor
	 * @param filePath		unused in the function
	 * @param fileName		unused in the function	
	 * @return String[]		a string array includes the command 
	 */
	public String[] assembleCommands(String filePath, String fileName) {
		ArrayList<String> commandArray = new ArrayList<String>();

		commandArray.add("sh");
		
		commandArray.add(m_shellScript);
		commandArray.add(m_fileName);
		commandArray.add(m_logFile);

		return commandArray.toArray(new String[commandArray.size()]);
	}
	
	/**
	 * Stores the input path as the shell script path.
	 * @param fileName	The path will be stored in the field m_shellScript
	 */
	public void setShellFile(String fileName)
	{
		m_shellScript = fileName;
	}
	
	/**
	 * Stores the string as the file name.
	 * @param fileName	The  will be stored in the field m_fileName
	 */
	public void setFileName(String fileName)
	{
		m_fileName = fileName;
	}
	
	/**
	 * Stores the input path as the log path.
	 * @param logFile	The path will be stored in the field m_logFile
	 */
	public void setLogFile(String logFile)
	{
		m_logFile = logFile;
	}
}
